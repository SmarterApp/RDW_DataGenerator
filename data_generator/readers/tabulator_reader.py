"""
A reader for the output of the assessment package tabulator.

It will produce assessment packages optionally with items.

"""

import csv

import datetime
from os import listdir
from os.path import isfile, join

from data_generator.config import cfg
from data_generator.model.assessment import Assessment
from data_generator.model.item import AssessmentItem
from data_generator.model.segment import AssessmentSegment
from data_generator.util.id_gen import IDGen


def load_assessments(root_dir, load_sum, load_ica, load_iab, load_items):
    """
    Load assessments from any csv file in the given directory
    
    :param root_dir: 
    :param load_sum: True to load summative assessments
    :param load_ica: True to load interim comprehensive assessments
    :param load_iab: True to load interim assessment blocks
    :param load_items: True to load items, False to ignore item data
    :return: 
    """
    assessments = []
    for file in (join(root_dir, f) for f in listdir(root_dir) if f.endswith('.csv') and isfile(join(root_dir, f))):
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

    asmt = None
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parse_asmt = False
            id = row['AssessmentId']
            if asmt and asmt.id == id:
                if not load_items:
                    continue
                # else fall thru and load row's item into current assessment
            else:
                type = row['AssessmentSubtype']
                if (not load_sum and type == 'SUM') or (not load_ica and type == 'ICA') or (not load_iab and type == 'IAB'):
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
        asmt.year = int(row['AcademicYear']) + 1  # TODO - remove +1 when tabulator is fixed
        asmt.bank_key = row['BankKey']
        asmt.overall_score_min = int(float(row['ScaledLow1']))
        asmt.overall_cut_point_1 = int(float(row['ScaledHigh1']))
        asmt.overall_cut_point_2 = int(float(row['ScaledHigh2']))
        asmt.overall_cut_point_3 = int(float(row['ScaledHigh3']))
        asmt.overall_cut_point_4 = None
        asmt.overall_score_max = int(float(row['ScaledHigh4']))
        # TODO - standard? what's in there?
        # TODO - claim/target? they'll need to be trimmed (trailing tab)
        # TODO - derive accommodations from 'ASL', 'Braille', 'AllowCalculator', etc.

        # this is silly but adheres to the way the generation framework currently works:
        # the assessment package has a period and that is used as the date taken; so we'll
        # follow the pattern and arbitrarily pick the first effective date for this year
        asmt.period = datetime.date(asmt.year - 1, 10, 1)
        # TODO - these dates should come from the assessment package, but not in CSV?
        asmt.effective_date = asmt.period
        asmt.from_date = asmt.period
        asmt.to_date = asmt.period

        # more stuff that doesn't really make sense but the framework currently requires
        # TODO - figure out how the claim stuff will work for realsies
        asmt.claim_1_score_min = cfg.CLAIM_SCORE_MIN
        asmt.claim_1_score_max = cfg.CLAIM_SCORE_MAX
        asmt.claim_1_score_weight = 1.0
        asmt.claim_2_score_min = 0
        asmt.claim_2_score_max = 0
        asmt.claim_2_score_weight = 0.0
        asmt.claim_3_score_min = 0
        asmt.claim_3_score_max = 0
        asmt.claim_3_score_weight = 0.0
        asmt.claim_perf_lvl_name_1 = cfg.CLAIM_PERF_LEVEL_NAME_1
        asmt.claim_perf_lvl_name_2 = cfg.CLAIM_PERF_LEVEL_NAME_2
        asmt.claim_perf_lvl_name_3 = cfg.CLAIM_PERF_LEVEL_NAME_3
        asmt.claim_cut_point_1 = cfg.CLAIM_SCORE_CUT_POINT_1
        asmt.claim_cut_point_2 = cfg.CLAIM_SCORE_CUT_POINT_2

        # if items are being parsed, create segment and list
        if parse_item:
            asmt.segment = AssessmentSegment()
            asmt.segment.id = IDGen.get_uuid()
            asmt.item_bank = []

    if parse_item:
        item = AssessmentItem()
        item.bank_key = row['BankKey']
        item.item_key = row['ItemId']
        item.type = row['ItemType']
        item.position = int(row['FormPosition'])
        item.segment_id = asmt.segment.id
        item.max_score = int(row['MaxPoints'])
        item.operational = '0' if row['IsFieldTest'] == 'true' else '1'
        asmt.item_bank.append(item)


def __mapAssessmentType(type, subtype):
    if subtype == 'IAB': return 'INTERIM ASSESSMENT BLOCK'
    if subtype == 'ICA': return 'INTERIM COMPREHENSIVE'
    if subtype == 'SUM': return 'SUMMATIVE'
    raise Exception('Unexpected assessment type {}-{}'.format(type, subtype))

def __mapSubject(subject):
    if subject.lower() == 'math': return 'Math'
    if subject.lower() == 'ela': return 'ELA'
    raise Exception('Unexpected assessment subject {}'.format(subject))

