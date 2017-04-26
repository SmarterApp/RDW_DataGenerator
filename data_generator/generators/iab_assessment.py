"""
An assessment generator
"""

import datetime
import random

import data_generator.config.cfg as sbac_config
import data_generator.generators.assessment as gen_asmt_generator
from data_generator.model.assessment import Assessment
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.interimassessment import InterimAssessment
from data_generator.model.interimassessmentoutcome import InterimAssessmentOutcome
from data_generator.model.student import Student
from data_generator.sbac_generators.hierarchy import InstitutionHierarchy
from data_generator.util.assessment_stats import Properties, RandomLevelByDemographics
from data_generator.util.id_gen import IDGen


def create_iab_outcome_object(date_taken: datetime.date,
                              student: Student,
                              iab_asmt: InterimAssessment,
                              inst_hier: InstitutionHierarchy,
                              id_gen: IDGen,
                              iab_results: {str: InterimAssessmentOutcome},
                              gen_item=True):
    """

    :param student:
    :param iab_asmt:
    :param inst_hier:
    :param id_gen:
    :param iab_results:
    :param gen_item:
    :return:
    """
    # Make sure the assessment is known in the results
    if iab_asmt.guid_sr not in iab_results:
        iab_results[iab_asmt.guid_sr] = []

    # Create the original outcome object
    ao = generate_interim_assessment_outcome(date_taken, student, iab_asmt, inst_hier, id_gen, gen_item=gen_item)
    iab_results[iab_asmt.guid_sr].append(ao)


def generate_interim_assessment(asmt_year: int,
                                subject: str,
                                block: str,
                                grade: int,
                                id_gen: IDGen,
                                claim_definitions=sbac_config.CLAIM_DEFINITIONS,
                                gen_item=True):
    """
    Generate an assessment object.

    @param asmt_year: Assessment year
    @param subject: Assessment subject
    @param block: block
    @param grade: grade
    @param id_gen: id generator
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

    # Set other specifics
    sa.rec_id = id_gen.get_rec_id('assessment')
    sa.guid_sr = id_gen.get_sr_uuid()
    sa.type = 'INTERIM ASSESSMENT BLOCK'
    sa.period = str(asmt_year-1)
    sa.year = asmt_year
    sa.version = sbac_config.ASMT_VERSION
    sa.name = 'SBAC-IAB-FIXED-G{}{}-{}-{}-{}'.format(grade, subject[0], ''.join(c for c in block if c.isupper()), subject, grade)
    sa.id = '(SBAC){}-{}-{}'.format(sa.name, asmt_year-1, asmt_year)
    sa.subject = subject
    sa.grade = grade
    sa.bank_key = '200'       # TODO - handle properly
    sa.claim_1_name = block
    sa.claim_2_name = "Grade %s" % grade
    sa.claim_3_name = None
    sa.claim_4_name = None
    sa.perf_lvl_name_1 = sbac_config.CLAIM_PERF_LEVEL_NAME_1
    sa.perf_lvl_name_2 = sbac_config.CLAIM_PERF_LEVEL_NAME_2
    sa.perf_lvl_name_3 = sbac_config.CLAIM_PERF_LEVEL_NAME_3
    sa.perf_lvl_name_4 = None
    sa.perf_lvl_name_5 = None
    sa.overall_score_min = sbac_config.ASMT_SCORE_MIN
    sa.overall_score_max = sbac_config.ASMT_SCORE_MAX
    sa.claim_1_score_min = sbac_config.CLAIM_SCORE_MIN
    sa.claim_1_score_max = sbac_config.CLAIM_SCORE_MAX
    sa.claim_1_score_weight = 1.0
    sa.claim_2_score_min = 0
    sa.claim_2_score_max = 0
    sa.claim_2_score_weight = 0.0
    sa.claim_3_score_min = 0
    sa.claim_3_score_max = 0
    sa.claim_3_score_weight = 0.0
    sa.claim_4_score_min = None
    sa.claim_4_score_max = None
    sa.claim_4_score_weight = None
    sa.claim_perf_lvl_name_1 = sbac_config.CLAIM_PERF_LEVEL_NAME_1
    sa.claim_perf_lvl_name_2 = sbac_config.CLAIM_PERF_LEVEL_NAME_2
    sa.claim_perf_lvl_name_3 = sbac_config.CLAIM_PERF_LEVEL_NAME_3
    sa.overall_cut_point_1 = sbac_config.ASMT_SCORE_CUT_POINT_1
    sa.overall_cut_point_2 = sbac_config.ASMT_SCORE_CUT_POINT_2
    sa.overall_cut_point_3 = sbac_config.ASMT_SCORE_CUT_POINT_3
    sa.overall_cut_point_4 = sbac_config.ASMT_SCORE_CUT_POINT_4
    sa.claim_cut_point_1 = sbac_config.CLAIM_SCORE_CUT_POINT_1
    sa.claim_cut_point_2 = sbac_config.CLAIM_SCORE_CUT_POINT_2
    sa.effective_date = datetime.date(asmt_year-1, 8, 15)
    sa.from_date = sa.effective_date
    sa.to_date = sbac_config.ASMT_TO_DATE
    gen_asmt_generator.generate_segment_and_item_bank(sa, gen_item, sbac_config.IAB_ITEM_BANK_SIZE, id_gen)

    return sa


def generate_interim_assessment_outcome(date_taken: datetime.date,
                                        student: Student,
                                        assessment: Assessment,
                                        inst_hier: InstitutionHierarchy,
                                        id_gen: IDGen,
                                        gen_item=True):
    """
    Generate an assessment outcome for a given student.

    @param student: The student to create the outcome for
    @param assessment: The assessment to create the outcome for
    @param inst_hier: The institution hierarchy this student belongs to
    @param id_gen: ID generator
    @param gen_item: If should create item-level responses
    @returns: The assessment outcome
    """

    # Run the General generator
    sao = gen_asmt_generator.generate_assessment_outcome(student, assessment, AssessmentOutcome)

    # Set other specifics
    sao.rec_id = id_gen.get_rec_id('assessment_outcome')
    sao.inst_hierarchy = inst_hier
    sao.date_taken = date_taken

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

    # The legacy output expects there to be a claim_1_score. But that is not correct for IABs, there should be just
    # an overall score. So we'll fill out both for now ...
    if gen_item:
        percent_points = sum(map(lambda aid: aid.score, sao.item_data)) / assessment.item_total_score
        sao.overall_score = (assessment.overall_score_max - assessment.overall_score_min) * percent_points + assessment.overall_score_min
    else:
        sao.overall_score = random.randint(assessment.overall_score_min, assessment.overall_score_max)
    sao.overall_score_range_min = max(assessment.overall_score_min, sao.overall_score - 20)
    sao.overall_score_range_max = min(assessment.overall_score_max, sao.overall_score + 20)
    sao.overall_perf_lvl = _pick_performance_level(sao.overall_score,
        (assessment.overall_cut_point_1, assessment.overall_cut_point_2, assessment.overall_cut_point_3))

    sao.claim_1_score = random.randint(assessment.claim_1_score_min, assessment.claim_1_score_max)
    sao.claim_1_score_range_min = max(sbac_config.CLAIM_SCORE_MIN, sao.claim_1_score - 20)
    sao.claim_1_score_range_max = min(sbac_config.CLAIM_SCORE_MAX, sao.claim_1_score + 20)
    sao.claim_1_perf_lvl = _pick_performance_level(sao.claim_1_score, (assessment.claim_cut_point_1, assessment.claim_cut_point_2))

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
