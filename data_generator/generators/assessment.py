"""Generate assessment elements.
"""
from datetime import timedelta, datetime, time
from random import choice, randrange, random

from data_generator.config.cfg import ASMT_ITEM_BANK_FORMAT, ITEM_ANSWER_RATE, ANSWER_CORRECT_RATE
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


def generate_segment_and_item_bank(gen_item, size, id_gen: IDGen):
    if not gen_item:
        return None, []

    segment = AssessmentSegment()
    segment.id = id_gen.get_uuid()

    item_bank = []
    for i in range(size):
        item = AssessmentItem()
        item.position = i+1
        item.bank_key = '200'   # TODO - handle properly
        item.item_key = str(id_gen.get_rec_id('asmt_item_id'))
        item.type = choice(ASMT_ITEM_BANK_FORMAT)
        item.segment_id = segment.id
        item.max_score = 1      # TODO - randomly make some >1
        item.operational = '1'  # TODO - randomly make some field tests?
        item_bank.append(item)
    return segment, item_bank


def generate_item_data(items: [AssessmentItem], student_id, date_taken):
    # given items, generate item response data
    if not items or len(items) == 0:
        return []

    item_data = []

    # TODO - emit only a subset of the items in the item bank?

    # TODO - score should be more complex than 1 or 0

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

        if item.type == 'MC':
            aid.page_time = randrange(1000, 15000)
            aid.response_value = choice(['A', 'B', 'C', 'D'])
        elif item.type == 'MS':
            aid.page_time = randrange(2000, 30000)
            aid.response_value = choice(['A', 'B', 'C', 'D'])
        else:
            aid.page_time = randrange(2000, 60000)
            aid.response_value = item.type + ' response'

        aid.score_status = 'SCORED'
        if random() < ITEM_ANSWER_RATE:
            aid.is_selected = '1'
            aid.score = item.max_score if random() < ANSWER_CORRECT_RATE else randrange(0, item.max_score)
        else:
            aid.is_selected = '0'
            aid.score = 0
            aid.response_value = None

        resp_date += timedelta(milliseconds=aid.page_time)
        aid.response_date = resp_date

        item_data.append(aid)

    return item_data


def set_opportunity_dates(outcome: [AssessmentOutcome]):
    if len(outcome.item_data) == 0:
        outcome.start_date = datetime.combine(outcome.date_taken, time(hour=randrange(7, 14)))
        outcome.submit_date = outcome.start_date + timedelta(minutes=randrange(45, 60))
    else:
        outcome.start_date = outcome.item_data[0].response_date
        outcome.submit_date = outcome.item_data[-1].response_date
    outcome.status_date = outcome.submit_date
