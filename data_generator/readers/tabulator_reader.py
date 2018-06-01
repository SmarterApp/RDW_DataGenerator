"""
A reader for the output of the assessment package tabulator.

It will produce assessment packages optionally with items.

"""

import csv
import datetime
import glob

from data_generator.config import cfg
from data_generator.model.assessment import Assessment
from data_generator.model.claim import Claim
from data_generator.model.item import AssessmentItem
from data_generator.model.segment import AssessmentSegment
from data_generator.util.id_gen import IDGen


def load_assessments(glob_pattern, load_sum, load_ica, load_iab, load_items):
    """
    Load assessments from any csv file in the given directory
    
    :param glob_pattern:
    :param load_sum: True to load summative assessments
    :param load_ica: True to load interim comprehensive assessments
    :param load_iab: True to load interim assessment blocks
    :param load_items: True to load items, False to ignore item data
    :return: 
    """
    assessments = []
    for file in (glob.glob(glob_pattern)):
        assessments.extend(load_assessments_file(file, load_sum, load_ica, load_iab, load_items))
    return assessments


def load_assessments_file(file, load_sum, load_ica, load_iab, load_items):
    """
    Load assessments from a single tabulator csv file
    
    :param file: path of file to read 
    :param load_sum: True to load summative assessments
    :param load_ica: True to load interim comprehensive assessments
    :param load_iab: True to load interim assessment blocks
    :param load_items: True to load items, False to ignore item data
    :return: 
    """
    assessments = []

    def should_process(subtype):
        return (subtype == 'SUM' and load_sum) or (subtype == 'ICA' and load_ica) or (subtype == 'IAB' and load_iab)

    asmt = None
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        # get out early if this doesn't look like an assessments file
        if 'AssessmentId' not in reader.fieldnames:
            return assessments

        for row in reader:
            parse_asmt = False
            id = row['AssessmentId']
            if asmt and asmt.id == id:
                if not load_items:
                    continue
                # else fall thru and load row's item into current assessment
            else:
                if not should_process(row['AssessmentSubtype']):
                    continue
                asmt = Assessment()
                assessments.append(asmt)
                parse_asmt = True
            __load_row(row, asmt, parse_asmt, load_items)

    return assessments


def __load_row(row, asmt: Assessment, parse_asmt, parse_item):
    if parse_asmt:
        asmt.id = row['AssessmentId']
        asmt.name = row['AssessmentName']
        asmt.subject = __mapSubject(row['AssessmentSubject'])
        asmt.grade = int(row['AssessmentGrade'])
        asmt.type = __mapAssessmentType(row['AssessmentType'], row['AssessmentSubtype'])
        asmt.version = row['AssessmentVersion']
        asmt.year = int(row['AcademicYear'])
        asmt.bank_key = row['BankKey']

        asmt_scale_scores = cfg.ASMT_SCALE_SCORE[asmt.subject][asmt.grade]
        asmt.overall_score_min = __getScore(row['ScaledLow1'], asmt_scale_scores[0])
        asmt.overall_cut_point_1 = __getScore(row['ScaledHigh1'], asmt_scale_scores[1])
        asmt.overall_cut_point_2 = __getScore(row['ScaledHigh2'], asmt_scale_scores[2])
        asmt.overall_cut_point_3 = __getScore(row['ScaledHigh3'], asmt_scale_scores[3])
        asmt.overall_score_max = __getScore(row['ScaledHigh4'], asmt_scale_scores[-1])

        # TODO - standard? what's in there?
        # TODO - claim/target? they'll need to be trimmed (trailing tab)

        asmt.effective_date = datetime.date(asmt.year - 1, 8, 15)
        asmt.from_date = asmt.effective_date
        asmt.to_date = cfg.ASMT_TO_DATE

        # claims (this is just using the hard-coded values from generator code)
        asmt.claim_perf_lvl_name_1 = cfg.CLAIM_PERF_LEVEL_NAME_1
        asmt.claim_perf_lvl_name_2 = cfg.CLAIM_PERF_LEVEL_NAME_2
        asmt.claim_perf_lvl_name_3 = cfg.CLAIM_PERF_LEVEL_NAME_3
        if not asmt.is_iab():
            asmt.claims = [Claim(claim['code'], claim['name'], asmt.overall_score_min, asmt.overall_score_max)
                           for claim in cfg.CLAIM_DEFINITIONS[asmt.subject]]

        # if items are being parsed, create segment and list
        if parse_item:
            asmt.segment = AssessmentSegment()
            asmt.segment.id = IDGen.get_uuid()
            asmt.item_bank = []
            asmt.item_total_score = 0

    # infer allowed accommodations even if not parsing items
    if len(row['ASL']) > 0:
        asmt.accommodations.add('AmericanSignLanguage')
    if len(row['Braille']) > 0:
        asmt.accommodations.add('Braille')
    if len(row['AllowCalculator']) > 0:
        asmt.accommodations.add('Calculator')
    if len(row['Spanish']) > 0:
        asmt.accommodations.add('Spanish')

    if parse_item:
        item = AssessmentItem()
        item.bank_key = row['BankKey']
        item.item_key = row['ItemId']
        item.type = row['ItemType']
        item.position = __getInt(row['ItemPosition'], 0)
        item.segment_id = asmt.segment.id
        item.max_score = int(row['MaxPoints'])
        item.dok = int(row['DOK'])
        item.difficulty = float(row['avg_b'])
        item.operational = '0' if row['IsFieldTest'] == 'true' else '1'
        item.answer_key = row['AnswerKey'] if 'AnswerKey' in row else None
        item.options_count = int(row['NumberOfAnswerOptions']) if 'NumberOfAnswerOptions' in row else 0
        item.target = row['ClaimContentTarget'].strip() if 'ClaimContentTarget' in row else None
        asmt.item_bank.append(item)
        asmt.item_total_score += item.max_score


def __mapAssessmentType(type, subtype):
    if subtype == 'IAB': return 'INTERIM ASSESSMENT BLOCK'
    if subtype == 'ICA': return 'INTERIM COMPREHENSIVE'
    if subtype == 'SUM': return 'SUMMATIVE'
    raise Exception('Unexpected assessment type {}-{}'.format(type, subtype))


def __mapSubject(subject):
    if subject.lower() == 'math': return 'Math'
    if subject.lower() == 'ela': return 'ELA'
    raise Exception('Unexpected assessment subject {}'.format(subject))


def __getScore(value, default_value):
    try:
        return int(float(value))
    except ValueError:
        return default_value


def __getInt(value, default_value):
    try:
        return int(value)
    except ValueError:
        return default_value