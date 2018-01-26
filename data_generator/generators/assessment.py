"""Generate assessment elements.
"""
import hashlib

from datetime import timedelta, datetime, time
from random import choice, randrange, random, sample, randint
from string import ascii_uppercase

from math import ceil

from data_generator.config import cfg
from data_generator.config.cfg import ASMT_ITEM_BANK_FORMAT, ITEM_ANSWER_RATE, ANSWER_CORRECT_RATE
from data_generator.generators import names, text
from data_generator.generators.text import RandomText
from data_generator.model.assessment import Assessment
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.item import AssessmentItem
from data_generator.model.itemdata import AssessmentOutcomeItemData
from data_generator.model.segment import AssessmentSegment
from data_generator.model.student import Student
from data_generator.util.id_gen import IDGen


def generate_assessment(sub_class=None):
    """Generate a data_generator assessment.

    :param sub_class: The sub-class of assessment to create (if requested, must be subclass of Assessment)
    :returns: The assessment object
    """
    # Create the object
    a = Assessment() if sub_class is None else sub_class()
    a.guid = IDGen.get_uuid()

    return a


def generate_assessment_outcome(student: Student, assessment: Assessment, sub_class=None):
    """Generate an assessment outcome for a given student.

    :param student: The student to create the outcome for
    :param assessment: The assessment to create the outcome for
    :param sub_class: The sub-class of assessment outcome to create (if requested, must be subclass of
                      AssessmentOutcome)
    :returns: The assessment outcome
    """
    # Create the object
    ao = AssessmentOutcome() if sub_class is None else sub_class()
    ao.guid = IDGen.get_uuid()
    ao.student = student
    ao.assessment = assessment

    return ao


def generate_segment_and_item_bank(asmt: Assessment, gen_item, size, id_gen: IDGen):
    if not gen_item:
        asmt.segment = None
        asmt.item_bank = []
        asmt.item_total_score = None
        return

    # make a set of difficulty ranges favoring easy (x2), moderate (x3), hard (x1)
    diff_low = -3.0
    diff_mod = -2.5 + 0.2 * asmt.grade
    diff_hard = -1.25 + 0.25 * asmt.grade
    diff_high = 4.0
    diff_ranges = [(diff_low, diff_mod), (diff_low, diff_mod), (diff_mod, diff_hard), (diff_mod, diff_hard), (diff_mod, diff_hard), (diff_hard, diff_high)]

    segment = AssessmentSegment()
    segment.id = id_gen.get_uuid()

    item_bank = []
    for i in range(size):
        item = AssessmentItem()
        item.position = i + 1
        item.bank_key = '200'   # TODO - handle properly
        item.item_key = str(id_gen.get_rec_id('asmt_item_id'))
        item.segment_id = segment.id
        item.type = choice(ASMT_ITEM_BANK_FORMAT)
        if item.type == 'MC':
            item.options_count = 4
            item.answer_key = choice(ascii_uppercase[0:4])
        if item.type == 'MS':
            item.options_count = 6
            item.answer_key = ','.join(sorted(sample(ascii_uppercase[0:6], 2)))
        item.max_score = 1
        item.dok = choice([1, 1, 1, 2, 2, 2, 3, 3, 4])
        dr = choice(diff_ranges)
        item.difficulty = dr[0] + random() * (dr[1] - dr[0])
        item.operational = '1'
        item_bank.append(item)

    asmt.segment = segment
    asmt.item_bank = item_bank
    asmt.item_total_score = sum(map(lambda i: i.max_score, item_bank))


def generate_item_data(items: [AssessmentItem], student_id, date_taken):
    # given items, generate item response data
    if not items or len(items) == 0:
        return []

    item_data = []

    # TODO - emit only a subset of the items in the item bank?

    admin_date = datetime.combine(date_taken, time(hour=randrange(7, 14)))
    resp_date = admin_date
    for item in items:
        aid = AssessmentOutcomeItemData()
        aid.item = item
        aid.student_id = student_id
        aid.number_visits = 1
        aid.page_number = 1
        aid.page_visits = 1
        aid.dropped = '0'
        aid.admin_date = admin_date
        aid.score_status = 'SCORED'

        if random() < ITEM_ANSWER_RATE:
            generate_response(aid, item)
        else:
            aid.page_time = randrange(1000, 5000)
            aid.is_selected = '0'
            aid.score = 0
            aid.response_value = None

        resp_date += timedelta(milliseconds=aid.page_time)
        aid.response_date = resp_date

        item_data.append(aid)

    return item_data


def generate_session(outcome: [AssessmentOutcome]):
    """ generate and set session based on date, student group for this subject
    """
    group = getattr(outcome.student, "group_%i_text" % (1 + cfg.SUBJECTS.index(outcome.assessment.subject),))
    if not outcome.date_taken and not group: return

    hasher = hashlib.sha1()
    if outcome.date_taken: hasher.update(str(outcome.date_taken).encode())
    if group: hasher.update(group.encode())
    hexdigest = hasher.hexdigest()
    # pick last name based on last 4 digits of digest and combine with first 4 digits
    outcome.session = names.PEOPLE_NAMES.last_names[int(hexdigest[-4:], 16)][:3].upper() + '-' + hexdigest[:4]


def set_opportunity_dates(outcome: [AssessmentOutcome]):
    if len(outcome.item_data) == 0:
        outcome.start_date = datetime.combine(outcome.date_taken, time(hour=randrange(7, 14)))
        outcome.submit_date = outcome.start_date + timedelta(minutes=randrange(45, 60))
    else:
        outcome.start_date = outcome.item_data[0].response_date
        outcome.submit_date = outcome.item_data[-1].response_date
    outcome.status_date = outcome.submit_date


def generate_response(aid: AssessmentOutcomeItemData, item: AssessmentItem):
    """ generate and set response-related fields in outcome

    :param aid outcome to set
    :param item outcome's item
    """
    # difficulty ranges from -3.0 to 10.0 (more or less)
    # difficulty cut points vary by asmt/subject/grade but approximately:
    #   easy:  < -2.5 + 0.2 * grade
    #   moderate: < -1.25 + 0.25 * grade
    # chance to answer correctly should be adjusted by difficulty (-3.0 -> .95, 10.0 -> .30)
    correct = random() < (ANSWER_CORRECT_RATE + (0 if not item.difficulty else -0.05 * item.difficulty))

    aid.is_selected = '1'
    if item.type == 'MC':       # multiple choice
        aid.page_time = 1000 * randrange(1, 15)
        if correct:
            aid.response_value = item.answer_key
            aid.score = item.max_score
        else:
            aid.response_value = choice(ascii_uppercase[0:item.options_count].replace(item.answer_key, ''))
            aid.score = 0
    elif item.type == 'MS':     # multi select
        aid.page_time = 1000 * randrange(2, 30)
        if correct:
            aid.response_value = item.answer_key
            aid.score = item.max_score
        else:
            wrong_answers = ascii_uppercase[0:item.options_count]
            for ch in item.answer_key.split(','): wrong_answers = wrong_answers.replace(ch, '')
            aid.response_value = ','.join(sorted(sample(ascii_uppercase[0:item.options_count].replace(item.answer_key[0], ''), 2)))
            aid.score = 0
    elif item.type == 'SA' or item.type == 'ER':     # short answer text response
        aid.page_time = 1000 * randrange(60, 300)
        aid.response_value = text.paragraph()
        if correct:
            aid.score = item.max_score
        else:
            aid.score = 0
    elif item.type == 'WER':    # writing extended response (lots of text, shorter for wrong answer; has sub-scores)
        aid.page_time = 1000 * randrange(120, 600)
        if correct:
            aid.response_value = generate_wer_response(randint(3, 8))
            aid.sub_scores = [randrange(1, 5), randrange(1, 5), randrange(0, 3)]
        else:
            aid.response_value = generate_wer_response(1)
            aid.sub_scores = [randrange(0, 2), randrange(0, 2), 0]
        aid.score = ceil((aid.sub_scores[0] + aid.sub_scores[1]) / 2.0) + aid.sub_scores[2]
    # elif item.type == 'EBSR':   # evidence-based selected response (letter response)
    # elif item.type == 'MI':     # match interaction (seems like choice of two for multiple statements)
    # elif item.type == 'HTQ':    # hot text (is answer the text choices or position? multi-select)
    # elif item.type == 'EQ':     # equation response ?
    # elif item.type == 'GI':     # grid item response ?
    # elif item.type == 'TI':     # table interaction ?
    else:
        aid.page_time = 1000 * randrange(2, 60)
        aid.response_value = ('good ' if correct else 'poor ') + item.type + ' response'
        aid.score = item.max_score if correct else randrange(0, item.max_score)


def generate_wer_response(paragraphs):
    rt = RandomText()
    return '\n\n'.join(('<p>\n' + rt.paragraph() + '\n</p>') for _ in range(paragraphs))