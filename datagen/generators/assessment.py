"""Generate assessment elements.
"""
import hashlib
from datetime import timedelta, datetime, time
from math import ceil
from random import choice, randrange, random, sample, randint
from string import ascii_uppercase

from datagen.config import cfg
from datagen.generators import names, text
from datagen.generators.text import RandomText
from datagen.model.assessment import Assessment
from datagen.model.assessmentoutcome import AssessmentOutcome
from datagen.model.item import AssessmentItem
from datagen.model.itemdata import AssessmentOutcomeItemData
from datagen.model.student import Student
from datagen.util.id_gen import IDGen


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
    # hack for custom subjects
    subject_code = assessment.subject_code if assessment.subject_code in cfg.SUBJECT_CODES else 'ELA'
    ao.acc_asl_video_embed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_asl_video_embed'][subject_code])
    ao.acc_print_on_demand_items_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_print_on_demand_items_nonembed'][subject_code])
    ao.acc_noise_buffer_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_noise_buffer_nonembed'][subject_code])
    ao.acc_braile_embed = _pick_accommodation_code(cfg.LEGACY_ACCOMMODATIONS['acc_braile_embed'][subject_code])
    ao.acc_closed_captioning_embed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_closed_captioning_embed'][subject_code])
    ao.acc_text_to_speech_embed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_text_to_speech_embed'][subject_code])
    ao.acc_abacus_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_abacus_nonembed'][subject_code])
    ao.acc_alternate_response_options_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_alternate_response_options_nonembed'][subject_code])
    ao.acc_calculator_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_calculator_nonembed'][subject_code])
    ao.acc_multiplication_table_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_multiplication_table_nonembed'][subject_code])
    ao.acc_print_on_demand_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_asl_video_embed'][subject_code])
    ao.acc_read_aloud_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_read_aloud_nonembed'][subject_code])
    ao.acc_scribe_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_scribe_nonembed'][subject_code])
    ao.acc_speech_to_text_nonembed = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_speech_to_text_nonembed'][subject_code])
    ao.acc_streamline_mode = _pick_accommodation_code(
        cfg.LEGACY_ACCOMMODATIONS['acc_streamline_mode'][subject_code])

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
    if 'Spanish' in assessment.accommodations and student.lang_code == 'spa' and student.prg_lep:
        ao.accommodations.append(('Language', 'ESN', 'Spanish'))
        ao.accommodations.append(('Translation', 'TDS_WL_ESNGlossary', 'Spanish'))

    return ao


def generate_item_data(outcome: AssessmentOutcome):
    # given items, generate item response data in the outcome
    outcome.item_data = []

    asmt = outcome.assessment
    items = asmt.item_bank
    if not items or len(items) == 0:
        return

    # answer rate depends on student capability
    capability = outcome.student.capability[asmt.subject_code] \
        if outcome.student.capability and asmt.subject_code in outcome.student.capability else None
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
    group = outcome.student.get_group(outcome.assessment.subject_code)
    if not outcome.date_taken and not group:
        return

    hasher = hashlib.sha1()
    if outcome.date_taken:
        hasher.update(str(outcome.date_taken).encode())
    if group:
        hasher.update(group.name.encode())
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
    if item.type == 'MC':  # multiple choice
        aid.page_time = 1000 * randrange(1, 15)
        if correct:
            aid.response_value = item.answer_key
            aid.score = item.max_score
        else:
            aid.response_value = choice(ascii_uppercase[0:item.options_count].replace(item.answer_key, ''))
            aid.score = 0
    elif item.type == 'MS':  # multi select
        aid.page_time = 1000 * randrange(2, 30)
        if correct:
            aid.response_value = item.answer_key
            aid.score = item.max_score
        else:
            wrong_answers = ascii_uppercase[0:item.options_count]
            for ch in item.answer_key.split(','):
                wrong_answers = wrong_answers.replace(ch, '')
            aid.response_value = ','.join(
                sorted(sample(ascii_uppercase[0:item.options_count].replace(item.answer_key[0], ''), 2)))
            aid.score = 0
    elif item.type == 'EBSR':  # evidence-based selected response
        # usually requires two responses, the second may be: not required, single choice, multi-select
        # answer key examples: "B;D", "D", "A;C,E"; options_count is always 0, max_score is 1
        aid.page_time = 1000 * randrange(10, 60)
        answers = item.answer_key.split(';')
        if correct:
            aid.response_value = _generate_ebsr_response(answers[0], answers[1] if len(answers) > 1 else None)
            aid.score = item.max_score
        else:
            wrong_answers = ascii_uppercase[0:4].replace(answers[0], '')
            wrong_answer = wrong_answers[randrange(len(wrong_answers))]
            # it doesn't really matter what the second value is, so just reuse the first answer
            aid.response_value = _generate_ebsr_response(wrong_answer, wrong_answer)
            aid.score = 0
    elif item.type == 'SA' or item.type == 'ER':  # short answer text response
        aid.page_time = 1000 * randrange(60, 300)
        aid.response_value = text.paragraph()
        if correct:
            aid.score = item.max_score
        else:
            aid.score = 0
    elif item.type == 'WER':  # writing extended response (lots of text, shorter for wrong answer; has sub-scores)
        aid.page_time = 1000 * randrange(120, 600)
        if correct:
            aid.response_value = _generate_wer_response(randint(3, 8))
            aid.sub_scores = [randrange(1, 5), randrange(1, 5), randrange(0, 3)]
        else:
            aid.response_value = _generate_wer_response(1)
            aid.sub_scores = [randrange(0, 2), randrange(0, 2), 0]
        aid.score = ceil((aid.sub_scores[0] + aid.sub_scores[1]) / 2.0) + aid.sub_scores[2]
    elif item.type == 'EQ':  # equation response
        aid.page_time = 1000 * randrange(10, 60)
        # note that this doesn't consider whether answer is correct or not, just hardcoded response
        aid.response_value = '<response> <math xmlns="http://www.w3.org/1998/Math/MathML"> <mstyle displaystyle="true"> <mn>2</mn> <mn>0</mn> <mn>1</mn> </mstyle> </math> </response>'
        aid.score = item.max_score if correct else randrange(0, item.max_score)
    elif item.type == 'HTQ':  # hot text
        aid.page_time = 1000 * randrange(10, 60)
        # note that this doesn't consider whether answer is correct or not, just hardcoded response
        aid.response_value = _generate_htq_response(item.item_key)
        aid.score = item.max_score if correct else randrange(0, item.max_score)
    elif item.type == 'MI':  # match interaction
        aid.page_time = 1000 * randrange(10, 60)
        # note that this doesn't consider whether answer is correct or not, just hardcoded response
        aid.response_value = _generate_mi_response(item.item_key)
        aid.score = item.max_score if correct else randrange(0, item.max_score)
    elif item.type == 'TI':  # table interaction
        aid.page_time = 1000 * randrange(10, 60)
        # note that this doesn't consider whether answer is correct or not, just hardcoded response
        aid.response_value = _generate_ti_response(item.item_key)
        aid.score = item.max_score if correct else randrange(0, item.max_score)
    # elif item.type == 'GI':     # grid item response ?
    else:
        aid.page_time = 1000 * randrange(2, 60)
        aid.response_value = ('good ' if correct else 'poor ') + item.type + ' response'
        aid.score = item.max_score if correct else randrange(0, item.max_score)


def _generate_wer_response(paragraphs):
    rt = RandomText()
    return '\n\n'.join(('<p>\n' + rt.paragraph() + '\n</p>') for _ in range(paragraphs))


def _generate_ebsr_response(answer1, answer2):
    response1 = '<response id="EBSR1"><value>' + answer1 + '</value></response>'
    response2 = ('<response id="EBSR2"><value>' + answer2 + '</value></response>') if answer2 else ''
    return '<itemResponse>' + response1 + response2 + '</itemResponse>'


HTQValueMap = {
    '96010': [1],
    '182822': [5],
    '182827': [3],
    '182835': [2],
    '182851': [5],
    '182854': [6],
    '182879': [1, 6],
    '182898': [2],
    '182936': [3, 6],
    '182951': [2],
    '182958': [2, 10],
    '182964': [2, 3, 5],
    '182966': [2, 3, 5],
    '182979': [3],
    '182994': [1],
    '183002': [2, 3, 5],
    '183018': [1, 4],
    '183040': [4, 6],
    '183043': [2, 3, 5],
    '183045': [5],
    '183052': [1, 6],
    '183060': [4],
    '183074': [6, 10],
    '183084': [1, 6],
    '183091': [2, 3, 8],
    '183093': [1, 4],
    '183145': [1, 6],
    '183154': [1, 6],
    '183187': [3, 7]
}


def _generate_htq_response(item_key):
    value = ''.join(['<value>' + str(v) + '</value>' for v in HTQValueMap[item_key]]) if item_key in HTQValueMap else ''
    return '<itemReponse><response id=\'1\'>' + value + '</response></itemResponse>'


MIValueMap = {
    '182637': ['1 a', '2 c', '3 b'],
    '182643': ['1 a', '2 a', '3 b'],
    '182646': ['1 a', '2 b'],
    '182666': ['1 a', '2 c', '3 b'],
    '182697': ['1 a', '2 c', '3 b', '4 c'],
    '182702': ['1 a', '2 c', '3 b', '4 c'],
    '182825': ['1 a', '2 c', '3 b'],
    '182830': ['1 a', '2 b', '3 b', '4 a'],
    '182863': ['1 a', '2 b', '3 b', '4 a'],
    '182944': ['1 a', '2 b', '3 d'],
    '182956': ['1 a', '2 b', '3 b', '4 a', '5 c'],
    '182982': ['1 a', '2 b', '3 b', '4 a', '5 a'],
    '183063': ['1 a', '2 c', '3 b'],
    '183082': ['1 a', '2 c'],
    '183086': ['1 a', '2 b', '3 c', '4 a'],
    '183133': ['1 a', '2 b', '3 c', '4 a'],
    '183270': ['1 a', '2 b', '3 c', '4 a'],
    '183272': ['1 a', '2 c', '3 b'],
    '183278': ['1 a', '2 b', '3 c', '4 a'],
    '183288': ['1 a', '2 b', '3 c', '4 a'],
    '183290': ['1 a', '2 b', '3 b'],
    '183312': ['1 a', '2 b', '3 c', '4 a'],
    '183344': ['1 a', '2 b', '3 b'],
    '183352': ['1 a', '2 b', '3 b', '4 a', '5 a', '6 b'],
    '183383': ['1 a', '2 b', '3 c', '4 a'],
    '183385': ['1 a', '2 b', '3 b'],
    '183387': ['1 a', '2 b', '3 b'],
    '183529': ['1 a', '2 b', '3 b'],
    '183531': ['1 a', '2 b', '3 b'],
    '183533': ['1 a', '2 b', '3 b'],
    '183535': ['1 a', '2 c', '3 b'],
    '183539': ['1 a', '2 b', '3 b'],
    '183541': ['1 a', '2 b', '3 b'],
    '183579': ['1 a', '2 b', '3 b'],
    '183581': ['1 a', '2 b', '3 c', '4 a'],
    '183585': ['1 a', '2 b', '3 b', '4 a', '5 a'],
    '183587': ['1 a', '2 b', '3 b'],
    '183603': ['1 a', '2 b', '3 b'],
    '183605': ['1 a', '2 c', '3 d'],
    '183611': ['1 a', '2 b', '3 b'],
    '183613': ['1 a', '2 b', '3 b', '4 a', '5 a'],
    '183625': ['1 a', '2 b', '3 b', '4 a', '5 a'],
    '183629': ['1 a', '2 b', '3 b'],
    '183679': ['1 a', '2 c', '3 d']
}


def _generate_mi_response(item_key):
    value = ''.join(['<value>' + v + '</value>' for v in MIValueMap[item_key]]) if item_key in MIValueMap else ''
    return '<itemReponse><response id="RESPONSE">' + value + '</response></itemResponse>'


TIValueMap = {
    '183499': '<tr><th id="col0"/><th id="col1"/></tr><tr><td>2</td><td/></tr><tr><td/><td/></tr><tr><td/><td/></tr><tr><td/><td>54</td></tr>',
    '183501': '<tr><th id="col0"/><th id="col1"/></tr><tr><td/><td/></tr><tr><td>4</td><td/></tr><tr><td/><td>9.25</td></tr><tr><td/><td>12.30</td></tr><tr><td>18</td><td/></tr>',
    '183415': '<tr><th id="col0"/><th id="col1"/><th id="col2"/><th id="col3"/></tr><tr><td/><td>45</td><td>78</td><td>85</td></tr><tr><td/><td>9</td><td>2</td><td>20</td></tr><tr><td/><td>6</td><td>3</td><td>9</td></tr>',
    '183555': '<tr><th id="col0"/><th id="col1"/></tr><tr><td/><td>5</td></tr><tr><td/><td>6</td></tr><tr><td/><td>7</td></tr><tr><td/><td>8</td></tr><tr><td/><td>9</td></tr>',
    '183246': '<tr><th id="col0"/><th id="col1"/><th id="col2"/><th id="col3"/></tr><tr><td/><td>18</td><td/><td/></tr><tr><td/><td>25</td><td/><td/></tr><tr><td/><td/><td/><td/></tr>',
    '183694': '<tr><th id="col0"/><th id="col1"/><th id="col2"/></tr><tr><td/><td>6</td><td>9</td></tr><tr><td/><td>0</td><td>3</td></tr>',
    '182798': '<tr><th id="col0"/><th id="col1"/><th id="col2"/><th id="col3"/></tr><tr><td/><td>6</td><td>8</td><td>20</td></tr>',
    '182803': '<tr><th id="col0"/><th id="col1"/><th id="col2"/></tr><tr><td/><td/><td>10:00 a.m.</td></tr><tr><td/><td>10:15 a.m.</td><td>10:30 a.m.</td></tr><tr><td/><td>10:30 a.m.</td><td>11:30 a.m.</td></tr><tr><td/><td>11:30 a.m.</td><td>1:00 p.m.</td></tr><tr><td/><td>1:00 p.m.</td><td/></tr><tr><td/><td/><td/></tr>',
    '183695': '<tr><th id="col0"/><th id="col1"/><th id="col2"/></tr><tr><td/><td>5</td><td>8</td></tr><tr><td/><td>10</td><td>3</td></tr><tr><td/><td>56</td><td>9</td></tr>'
}


def _generate_ti_response(item_key):
    table = TIValueMap[item_key] if item_key in TIValueMap else ''
    return '<responseSpec><responseTable>' + table + '</responseTable></responseSpec>'


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
        raise ValueError('invalid default_code \'{}\' (must be 0 or 4)'.format(default_code))
