"""
An assessment generator for the SBAC assessment.

"""

import datetime
import random

import data_generator.config.cfg as sbac_config
import data_generator.config.cfg as sbac_in_config
import data_generator.config.hierarchy as hierarchy_config
import data_generator.generators.assessment as gen_asmt_generator
from data_generator.model.assessment import Assessment
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.institutionhierarchy import InstitutionHierarchy
from data_generator.model.student import Student
from data_generator.util.assessment_stats import Properties, RandomLevelByDemographics
from data_generator.util.assessment_stats import adjust_score
from data_generator.util.assessment_stats import random_claims
from data_generator.util.assessment_stats import random_score_given_level


def create_assessment_outcome_object(student, asmt, inst_hier, id_gen, assessment_results,
                                     skip_rate=sbac_in_config.ASMT_SKIP_RATE,
                                     retake_rate=sbac_in_config.ASMT_RETAKE_RATE,
                                     delete_rate=sbac_in_config.ASMT_DELETE_RATE,
                                     update_rate=sbac_in_config.ASMT_UPDATE_RATE,
                                     gen_item=True):
    """
    Create the outcome(s) for a single assessment for a student. If the student is determined to have skipped the
    assessment, the resulting array will be empty. Otherwise, one outcome will be created with the chance that a second
    outcome is also created. A second outcome will be created if the assessment is re-taken or updated. If the
    assessment is determined to have been deleted, no second record will be created.

    @param student: The student to create an outcome for
    @param asmt: The assessment to create an outcome for
    @param inst_hier: The institution hierarchy this assessment relates to
    @param id_gen: ID generator
    @param assessment_results: Dictionary of assessment results to update
    @param skip_rate: The rate (chance) that this student skips the assessment
    @param retake_rate: The rate (chance) that this student will re-take the assessment
    @param delete_rate: The rate (chance) that this student's result will be deleted
    @param update_rate: The rate (chance) that this student's result will be updated (deleted and re-added)
    @param gen_item: If should generate item-level data
    @returns: Array of outcomes
    """
    # Make sure they are taking the assessment
    if random.random() < skip_rate:
        return

    # Make sure the assessment is known in the results
    if asmt.guid_sr not in assessment_results:
        assessment_results[asmt.guid_sr] = []

    # Create the original outcome object
    ao = generate_assessment_outcome(student, asmt, inst_hier, id_gen,
                                     gen_item=gen_item)
    assessment_results[asmt.guid_sr].append(ao)

    # Decide if something special is happening
    special_random = random.random()
    if special_random < retake_rate:
        # Set the original outcome object to inactive, create a new outcome (with an advanced date take), and return
        ao.result_status = sbac_in_config.ASMT_STATUS_INACTIVE
        ao2 = generate_assessment_outcome(student, asmt, inst_hier, id_gen,
                                          gen_item=gen_item)
        assessment_results[asmt.guid_sr].append(ao2)
        ao2.date_taken += datetime.timedelta(days=5)
    elif special_random < update_rate:
        # Set the original outcome object to deleted and create a new outcome
        ao.result_status = sbac_in_config.ASMT_STATUS_DELETED
        ao2 = generate_assessment_outcome(student, asmt, inst_hier, id_gen,
                                          gen_item=gen_item)
        assessment_results[asmt.guid_sr].append(ao2)

        # See if the updated record should be deleted
        if random.random() < delete_rate:
            ao2.result_status = sbac_in_config.ASMT_STATUS_DELETED
    elif special_random < delete_rate:
        # Set the original outcome object to deleted
        ao.result_status = sbac_in_config.ASMT_STATUS_DELETED


def generate_assessment(type, period, asmt_year, subject, grade, id_gen, from_date=None, to_date=None,
                        claim_definitions=sbac_config.CLAIM_DEFINITIONS,
                        gen_item=True):
    """
    Generate an assessment object.

    @param type: Assessment type
    @param period: Period within assessment year
    @param asmt_year: Assessment year
    @param subject: Assessment subject
    @param grade: Assessment grade
    @param id_gen: ID generator
    @param from_date: Assessment from date
    @param to_date: Assessment to date
    @param claim_definitions: Definitions for claims to generate
    @param gen_item: If should create item-level item bank
    @returns: The assessment object
    """
    # Get the claim definitions for this subject
    if subject not in claim_definitions:
        raise KeyError("Subject '%s' not found in claim definitions" % subject)

    claims = claim_definitions[subject]

    # Run the General generator
    sa = gen_asmt_generator.generate_assessment(Assessment)

    # Determine the period month
    year_adj = 1
    period_month = 9
    if type == 'SUMMATIVE':
        year_adj = 0
        period_month = 5
    elif 'Winter' in period:
        period_month = 12
    elif 'Spring' in period:
        year_adj = 0
        period_month = 3

    # Set other specifics
    sa.name = 'SBAC-{}-{}'.format(subject, grade)
    sa.id = '(SBAC){}-{}-{}-{}'.format(sa.name, period, asmt_year-1, asmt_year)
    sa.subject = subject
    sa.grade = grade
    sa.rec_id = id_gen.get_rec_id('assessment')
    sa.guid_sr = id_gen.get_sr_uuid()
    sa.type = type
    sa.period = period + ' ' + str((asmt_year - year_adj))
    sa.year = asmt_year
    sa.version = sbac_config.ASMT_VERSION
    sa.subject = subject
    sa.bank_key = '200'   # TODO - handle properly
    sa.claim_1_name = claims[0]['name']
    sa.claim_2_name = claims[1]['name']
    sa.claim_3_name = claims[2]['name']
    sa.claim_4_name = claims[3]['name'] if len(claims) == 4 else None
    sa.perf_lvl_name_1 = sbac_config.ASMT_PERF_LEVEL_NAME_1
    sa.perf_lvl_name_2 = sbac_config.ASMT_PERF_LEVEL_NAME_2
    sa.perf_lvl_name_3 = sbac_config.ASMT_PERF_LEVEL_NAME_3
    sa.perf_lvl_name_4 = sbac_config.ASMT_PERF_LEVEL_NAME_4
    sa.perf_lvl_name_5 = sbac_config.ASMT_PERF_LEVEL_NAME_5
    sa.overall_score_min = sbac_config.ASMT_SCORE_MIN
    sa.overall_score_max = sbac_config.ASMT_SCORE_MAX
    sa.claim_1_score_min = sbac_config.CLAIM_SCORE_MIN
    sa.claim_1_score_max = sbac_config.CLAIM_SCORE_MAX
    sa.claim_1_score_weight = claims[0]['weight']
    sa.claim_2_score_min = sbac_config.CLAIM_SCORE_MIN
    sa.claim_2_score_max = sbac_config.CLAIM_SCORE_MAX
    sa.claim_2_score_weight = claims[1]['weight']
    sa.claim_3_score_min = sbac_config.CLAIM_SCORE_MIN
    sa.claim_3_score_max = sbac_config.CLAIM_SCORE_MAX
    sa.claim_3_score_weight = claims[2]['weight']
    sa.claim_4_score_min = sbac_config.CLAIM_SCORE_MIN if len(claims) == 4 else None
    sa.claim_4_score_max = sbac_config.CLAIM_SCORE_MAX if len(claims) == 4 else None
    sa.claim_4_score_weight = claims[3]['weight'] if len(claims) == 4 else None
    sa.claim_perf_lvl_name_1 = sbac_config.CLAIM_PERF_LEVEL_NAME_1
    sa.claim_perf_lvl_name_2 = sbac_config.CLAIM_PERF_LEVEL_NAME_2
    sa.claim_perf_lvl_name_3 = sbac_config.CLAIM_PERF_LEVEL_NAME_3
    sa.overall_cut_point_1 = sbac_config.ASMT_SCORE_CUT_POINT_1
    sa.overall_cut_point_2 = sbac_config.ASMT_SCORE_CUT_POINT_2
    sa.overall_cut_point_3 = sbac_config.ASMT_SCORE_CUT_POINT_3
    sa.overall_cut_point_4 = sbac_config.ASMT_SCORE_CUT_POINT_4
    sa.claim_cut_point_1 = sbac_config.CLAIM_SCORE_CUT_POINT_1
    sa.claim_cut_point_2 = sbac_config.CLAIM_SCORE_CUT_POINT_2
    sa.effective_date = datetime.date(asmt_year - year_adj, period_month, 15)
    sa.from_date = from_date if from_date is not None else sa.effective_date
    sa.to_date = to_date if to_date is not None else sbac_config.ASMT_TO_DATE
    sa.segment, sa.item_bank = gen_asmt_generator.generate_segment_and_item_bank(gen_item, sbac_config.ASMT_ITEM_BANK_SIZE, id_gen)

    return sa


def generate_assessment_outcome(student: Student, assessment: Assessment, inst_hier: InstitutionHierarchy,
                                id_gen, gen_item=True):
    """
    Generate an assessment outcome for a given student.

    @param student: The student to create the outcome for
    @param assessment: The assessment to create the outcome for
    @param inst_hier: The institution hierarchy this student belongs to
    @param id_gen: ID generator
    @param gen_item: If should create item-level responses
    @returns: The assessment outcome
    """
    # Create cut-point lists
    overall_cut_points = [assessment.overall_cut_point_1, assessment.overall_cut_point_2,
                          assessment.overall_cut_point_3]
    if assessment.overall_cut_point_4 is not None:
        overall_cut_points.append(assessment.overall_cut_point_4)
    claim_cut_points = [assessment.claim_cut_point_1, assessment.claim_cut_point_2]

    # Run the General generator
    sao = gen_asmt_generator.generate_assessment_outcome(student, assessment, AssessmentOutcome)

    # Set other specifics
    sao.rec_id = id_gen.get_rec_id('assessment_outcome')
    sao.inst_hierarchy = inst_hier

    # Create the date taken
    year_adj = 1
    period_month = 9
    if assessment.type == 'SUMMATIVE':
        year_adj = 0
        period_month = 5
    elif 'Winter' in assessment.period:
        period_month = 12
    elif 'Spring' in assessment.period:
        year_adj = 0
        period_month = 3
    sao.date_taken = datetime.date(assessment.year - year_adj, period_month, 15)

    # Generate assessment outcome Item-level data
    sao.item_data = [] if not gen_item else \
        gen_asmt_generator.generate_item_data(assessment.item_bank, student.guid_sr, sao.date_taken)

    # set timestamps for the opportunity
    gen_asmt_generator.set_opportunity_dates(sao)

    demographics = sbac_config.DEMOGRAPHICS_BY_GRADE[student.grade]
    level_breakdowns = sbac_config.LEVELS_BY_GRADE_BY_SUBJ[assessment.subject][student.grade]
    level_generator = RandomLevelByDemographics(demographics, level_breakdowns)

    student_race = ('dmg_eth_2mr' if student.eth_multi else
                    'dmg_eth_ami' if student.eth_amer_ind else
                    'dmg_eth_asn' if student.eth_asian else
                    'dmg_eth_blk' if student.eth_black else
                    'dmg_eth_hsp' if student.eth_hispanic else
                    'dmg_eth_pcf' if student.eth_pacific else
                    'dmg_eth_wht' if student.eth_white else
                    'dmg_eth_nst')

    student_demographics = Properties(dmg_prg_504=student.prg_sec504,
                                      dmg_prg_tt1=student.prg_econ_disad,
                                      dmg_prg_iep=student.prg_iep,
                                      dmg_prg_lep=student.prg_lep,
                                      gender=student.gender,
                                      race=student_race)

    sao.overall_perf_lvl = level_generator.random_level(student_demographics) + 1
    raw_overall_score = random_score_given_level(sao.overall_perf_lvl - 1,
                                                 [sbac_config.ASMT_SCORE_MIN] +
                                                 overall_cut_points +
                                                 [sbac_config.ASMT_SCORE_MAX])

    school_type = student.school.type_str
    adjustment = hierarchy_config.SCHOOL_TYPES[school_type]['students'].get('adjust_pld', 0.0)
    sao.overall_score = adjust_score(raw_overall_score, adjustment,
                                     sbac_config.ASMT_SCORE_MIN, sbac_config.ASMT_SCORE_MAX)

    overall_range_min = random.randint(50, 100)  # Total score range is between 100 and 200 points around score
    overall_range_max = random.randint(50, 100)  # Total score range is between 100 and 200 points around score
    sao.overall_score_range_min = max(sbac_config.ASMT_SCORE_MIN, sao.overall_score - overall_range_min)
    sao.overall_score_range_max = min(sbac_config.ASMT_SCORE_MAX, sao.overall_score + overall_range_max)

    claims = sbac_config.CLAIM_DEFINITIONS[assessment.subject]
    claim_weights = [claim['weight'] for claim in claims]
    claim_scores = random_claims(sao.overall_score, claim_weights, sbac_config.CLAIM_SCORE_MIN,
                                 sbac_config.CLAIM_SCORE_MAX)

    sao.claim_1_score = claim_scores[0]
    sao.claim_1_score_range_min = max(sbac_config.CLAIM_SCORE_MIN, sao.claim_1_score - 20)
    sao.claim_1_score_range_max = min(sbac_config.CLAIM_SCORE_MAX, sao.claim_1_score + 20)
    sao.claim_1_perf_lvl = _pick_performance_level(sao.claim_1_score, claim_cut_points)

    sao.claim_2_score = claim_scores[1]
    sao.claim_2_score_range_min = max(sbac_config.CLAIM_SCORE_MIN, sao.claim_2_score - 20)
    sao.claim_2_score_range_max = min(sbac_config.CLAIM_SCORE_MAX, sao.claim_2_score + 20)
    sao.claim_2_perf_lvl = _pick_performance_level(sao.claim_2_score, claim_cut_points)

    sao.claim_3_score = claim_scores[2]
    sao.claim_3_score_range_min = max(sbac_config.CLAIM_SCORE_MIN, sao.claim_3_score - 20)
    sao.claim_3_score_range_max = min(sbac_config.CLAIM_SCORE_MAX, sao.claim_3_score + 20)
    sao.claim_3_perf_lvl = _pick_performance_level(sao.claim_3_score, claim_cut_points)

    if assessment.claim_4_name is not None:
        if len(claim_scores) != 4:
            raise Exception(
                "unexpected number of claim scores: %s %s %s" % (assessment.subject, claim_scores, claim_weights))

        sao.claim_4_score = claim_scores[3]
        sao.claim_4_score_range_min = max(sbac_config.CLAIM_SCORE_MIN, sao.claim_4_score - 20)
        sao.claim_4_score_range_max = min(sbac_config.CLAIM_SCORE_MAX, sao.claim_4_score + 20)
        sao.claim_4_perf_lvl = _pick_performance_level(sao.claim_4_score, claim_cut_points)

    elif len(claim_scores) != 3:
        raise Exception(
            "unexpected number of claim scores: %s %s %s" % (assessment.subject, claim_scores, claim_weights))

    # Create accommodations details
    sao.acc_asl_video_embed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_asl_video_embed'][assessment.subject])
    sao.acc_print_on_demand_items_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_print_on_demand_items_nonembed'][assessment.subject])
    sao.acc_noise_buffer_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_noise_buffer_nonembed'][assessment.subject])
    sao.acc_braile_embed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_braile_embed'][assessment.subject])
    sao.acc_closed_captioning_embed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_closed_captioning_embed'][assessment.subject])
    sao.acc_text_to_speech_embed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_text_to_speech_embed'][assessment.subject])
    sao.acc_abacus_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_abacus_nonembed'][assessment.subject])
    sao.acc_alternate_response_options_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_alternate_response_options_nonembed'][assessment.subject])
    sao.acc_calculator_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_calculator_nonembed'][assessment.subject])
    sao.acc_multiplication_table_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_multiplication_table_nonembed'][assessment.subject])
    sao.acc_print_on_demand_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_asl_video_embed'][assessment.subject])
    sao.acc_read_aloud_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_read_aloud_nonembed'][assessment.subject])
    sao.acc_scribe_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_scribe_nonembed'][assessment.subject])
    sao.acc_speech_to_text_nonembed = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_speech_to_text_nonembed'][assessment.subject])
    sao.acc_streamline_mode = _pick_default_accommodation_code(
        sbac_config.ACCOMMODATIONS['acc_streamline_mode'][assessment.subject])

    return sao


def _pick_performance_level(score, cut_points):
    """
    Pick the performance level for a given score and cut points.

    @param score: The score to assign a performance level for
    @param cut_points: List of scores that separate the performance levels
    @returns: Performance level
    """
    for i, cut_point in enumerate(cut_points):
        if score < cut_point:
            return i + 1

    return len(cut_points) + 1


def _pick_default_accommodation_code(default_code):
    """
    Pick a random accommodation code between 4 and 26 inclusive if default_code is 4.
    If code is 0 return 0.

    @param default_code: The default code from configuration
    @return: Generated random code
    """
    if default_code == 0:
        return 0
    elif default_code == 4:
        return random.randint(4, 26)
    else:
        raise ValueError('invalid default_code \'%s\' (must be 0 or 4)' % (default_code,))
