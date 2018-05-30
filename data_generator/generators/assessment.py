"""Generate assessment elements.
"""
import hashlib
from datetime import timedelta, datetime, time
from math import ceil
from random import choice, randrange, random, sample, randint
from string import ascii_uppercase

from data_generator.config import cfg
from data_generator.config.cfg import ASMT_ITEM_BANK_FORMAT
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


def generate_assessment_outcome(student: Student, assessment: Assessment, id_gen: IDGen):
    """Generate an assessment outcome for a given student.

    :param student: The student to create the outcome for
    :param assessment: The assessment to create the outcome for
    :param id_gen: ID generator
    :returns: The assessment outcome
    """
    # Create the object
    ao = AssessmentOutcome()
    ao.guid = IDGen.get_uuid()
    ao.student = student
    ao.assessment = assessment

    # Set common behaviors 
    # Be careful, there is some order dependency that mean most of this happens in the sub-generators
    ao.rec_id = id_gen.get_rec_id('assessment_outcome')

    # Create legacy accommodations details
    ao.acc_asl_video_embed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_asl_video_embed'][assessment.subject])
    ao.acc_print_on_demand_items_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_print_on_demand_items_nonembed'][assessment.subject])
    ao.acc_noise_buffer_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_noise_buffer_nonembed'][assessment.subject])
    ao.acc_braile_embed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_braile_embed'][assessment.subject])
    ao.acc_closed_captioning_embed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_closed_captioning_embed'][assessment.subject])
    ao.acc_text_to_speech_embed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_text_to_speech_embed'][assessment.subject])
    ao.acc_abacus_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_abacus_nonembed'][assessment.subject])
    ao.acc_alternate_response_options_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_alternate_response_options_nonembed'][assessment.subject])
    ao.acc_calculator_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_calculator_nonembed'][assessment.subject])
    ao.acc_multiplication_table_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_multiplication_table_nonembed'][assessment.subject])
    ao.acc_print_on_demand_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_asl_video_embed'][assessment.subject])
    ao.acc_read_aloud_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_read_aloud_nonembed'][assessment.subject])
    ao.acc_scribe_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_scribe_nonembed'][assessment.subject])
    ao.acc_speech_to_text_nonembed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_speech_to_text_nonembed'][assessment.subject])
    ao.acc_streamline_mode = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_streamline_mode'][assessment.subject])

    # Create real accommodations based on assessment and other data.
    # Yeah, this should be driven by configuration at some point but for now, let's get a couple emitted ...
    # FYI, student disability codes:
    # DB (Deaf-blindness)
    # HI (Hearing impairment)
    # MD (multiple disabilities)
    # SLI (speech or language impairment)
    # VI (visual impairment)
    if 'AmericanSignLanguage' in assessment.accommodations and student.prg_primary_disability in ('DB', 'HI', 'MD'):
        ao.accommodations.append(('AmericanSignLanguage', 'TDS_ASL1', 'Show ASL videos'))
    if 'Braille' in assessment.accommodations and student.prg_primary_disability in ('DB', 'MD', 'VI'):
        ao.accommodations.append(('BrailleType', 'TDS_BT_UCT', 'UEB'))
    if 'Calculator' in assessment.accommodations:
        ao.accommodations.append(('Calculator', 'TDS_CalcBasic', 'Calculator on'))
        ao.accommodations.append(('Non-Embedded Accommodations', 'NEA_Calc', 'Calculator'))
    if 'Spanish' in assessment.accommodations and student.lang_code == 'esp':
        ao.accommodations.append(('Language', 'ESN', 'Spanish'))
        ao.accommodations.append(('Translation', 'TDS_WL_ESNGlossary', 'Spanish'))

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
        item.bank_key = '200'
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


def generate_item_data(outcome: AssessmentOutcome):
    # given items, generate item response data in the outcome
    outcome.item_data = []

    asmt = outcome.assessment
    items = asmt.item_bank
    if not items or len(items) == 0:
        return

    # answer rate depends on student capability
    capability = outcome.student.capability[asmt.subject] if outcome.student.capability and asmt.subject in outcome.student.capability else None
    answer_rate = (0.88 + 0.03 * capability) if capability is not None else 0.94
    admin_date = datetime.combine(outcome.date_taken, time(hour=randrange(7, 14)))
    resp_date = admin_date

    for item in items:
        aid = AssessmentOutcomeItemData()
        aid.item = item
        aid.number_visits = 1
        aid.page_number = 1
        aid.page_visits = 1
        aid.dropped = '0'
        aid.admin_date = admin_date
        aid.score_status = 'SCORED'

        if random() < answer_rate:
            generate_response(aid, item, capability)
        else:
            aid.page_time = randrange(1000, 5000)
            aid.is_selected = '0'
            aid.score = 0
            aid.response_value = None

        resp_date += timedelta(milliseconds=aid.page_time)
        aid.response_date = resp_date

        outcome.item_data.append(aid)


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


def generate_response(aid: AssessmentOutcomeItemData, item: AssessmentItem, capability: float = None):
    """ generate and set response-related fields in outcome

    :param aid outcome to set
    :param item outcome's item
    :param capability student's capability (0.0 - 4.0)
    """
    # difficulty ranges from -3.0 to 10.0 (more or less)
    # difficulty cut points vary by asmt/subject/grade but approximately:
    #   easy:  < -2.5 + 0.2 * grade
    #   moderate: < -1.25 + 0.25 * grade
    # chance to answer correctly is adjusted by difficulty (-3.0 -> +0.15, 10.0 -> -0.50)
    #
    # student capability ranges from 0.0 to 4.0
    # chance to answer correctly is based on capability if it's available
    correct_rate = (0.40 + 0.15 * capability) if capability is not None else 0.70
    correct_rate += (0 if not item.difficulty else -0.05 * item.difficulty)
    correct = random() < correct_rate

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


def _pick_accommodation_code(default_code):
    """
    Pick a random accommodation code between 4 and 26 inclusive if default_code is 4.
    If code is 0 return 0.

    @param default_code: The default code from configuration
    @return: Generated random code
    """
    if default_code == 0:
        return 0
    elif default_code == 4:
        return randint(4, 26)
    else:
        raise ValueError('invalid default_code \'%s\' (must be 0 or 4)' % (default_code,))
