"""
An assessment generator
"""

import datetime
import random
from collections import OrderedDict

import data_generator.config.cfg as sbac_config
import data_generator.generators.assessment as gen_asmt_generator
from data_generator.sbac_generators.hierarchy import InstitutionHierarchy
from data_generator.model.itemdata import AssessmentOutcomeItemData
from data_generator.model.student import Student
from data_generator.model.assessment import Assessment
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.util.assessment_stats import Properties, RandomLevelByDemographics
from data_generator.util.id_gen import IDGen


def generate_interim_assessment(date: datetime.date,
                                asmt_year: int,
                                subject: str,
                                block: str,
                                grade: int,
                                id_gen: IDGen,
                                claim_definitions=sbac_config.CLAIM_DEFINITIONS,
                                generate_item_level=True):
    """
    Generate an assessment object.

    @param date: Assessment to date
    @param asmt_year: Assessment year
    @param subject: Assessment subject
    @param block: block
    @param grade: grade
    @param id_gen: id generator
    @param claim_definitions: Definitions for claims to generate
    @param generate_item_level: If should create item-level item bank
    @returns: The assessment object
    """
    # Get the claim definitions for this subject
    if subject not in claim_definitions:
        raise KeyError("Subject '%s' not found in claim definitions" % subject)

    claims = claim_definitions[subject]

    # Run the General generator
    sa = gen_asmt_generator.generate_assessment(Assessment)

    # Generate Assessment Item Bank
    item_bank = {}
    if generate_item_level:
        for i in range(1, sbac_config.ASMT_ITEM_BANK_SIZE + 1):
            item_bank[i] = id_gen.get_rec_id('assmt_item_id')

    # Set other specifics
    sa.rec_id = id_gen.get_rec_id('assessment')
    sa.guid_sr = id_gen.get_sr_uuid()
    sa.asmt_type = "INTERIM ASSESSMENT BLOCKS"
    sa.period = str(date)
    sa.period_year = asmt_year
    sa.version = sbac_config.ASMT_VERSION
    sa.subject = subject
    sa.claim_1_name = block
    sa.claim_2_name = "Grade %s" % grade
    sa.claim_3_name = None
    sa.claim_4_name = None
    sa.perf_lvl_name_1 = None
    sa.perf_lvl_name_2 = None
    sa.perf_lvl_name_3 = None
    sa.perf_lvl_name_4 = None
    sa.perf_lvl_name_5 = None
    sa.overall_score_min = 0
    sa.overall_score_max = 0
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
    sa.overall_cut_point_1 = None
    sa.overall_cut_point_2 = None
    sa.overall_cut_point_3 = None
    sa.overall_cut_point_4 = None
    sa.claim_cut_point_1 = sbac_config.CLAIM_SCORE_CUT_POINT_1
    sa.claim_cut_point_2 = sbac_config.CLAIM_SCORE_CUT_POINT_2
    sa.effective_date = date
    sa.from_date = date
    sa.to_date = date
    sa.item_bank = item_bank

    return sa

#TODO why summative is here?

def generate_interim_assessment_outcome(student: Student,
                                        assessment: Assessment,
                                        inst_hier: InstitutionHierarchy,
                                        id_gen: IDGen,
                                        generate_item_level=True):
    """
    Generate an assessment outcome for a given student.

    @param student: The student to create the outcome for
    @param assessment: The assessment to create the outcome for
    @param inst_hier: The institution hierarchy this student belongs to
    @param id_gen: ID generator
    @param generate_item_level: If should create item-level responses
    @returns: The assessment outcome
    """
    # Create cut-point lists
    claim_cut_points = [assessment.claim_cut_point_1, assessment.claim_cut_point_2]

    # Run the General generator
    sao = gen_asmt_generator.generate_assessment_outcome(student, assessment, AssessmentOutcome)

    # Set other specifics
    sao.rec_id = id_gen.get_rec_id('assessment_outcome')
    sao.inst_hierarchy = inst_hier

    # Generate assessment outcome Item-level data
    if generate_item_level:
        item_data_dict = {}
        for i in range(1, sbac_config.ITEMS_PER_ASMT + 1):
            pos_item = random.choice(list(assessment.item_bank.keys()))
            while pos_item in item_data_dict:
                pos_item = random.choice(list(assessment.item_bank.keys()))
            item_id = assessment.item_bank[pos_item]
            item_data_dict[pos_item] = item_id

        od = OrderedDict(sorted(item_data_dict.items()))

        segment_id = '(SBAC)SBAC-MG110PT-S2-' + assessment.subject + '-' + str(student.grade) + '-' + \
                     assessment.period[0:-5] + '-' + str(assessment.period_year - 1) + '-' + str(assessment.period_year)

        for pos in od:
            item_format = random.choice(sbac_config.ASMT_ITEM_BANK_FORMAT)
            item_level_data = AssessmentOutcomeItemData()
            item_level_data.student_id = student.guid_sr
            item_level_data.key = od[pos]
            item_level_data.segment_id = segment_id
            item_level_data.position = pos
            item_level_data.format = item_format
            sao.item_level_data.append(item_level_data)

    # Create the date taken
    sao.date_taken = assessment.period

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

    sao.claim_1_score = random.randint(assessment.claim_1_score_min, assessment.claim_1_score_max)
    sao.claim_1_score_range_min = max(sbac_config.CLAIM_SCORE_MIN, sao.claim_1_score - 20)
    sao.claim_1_score_range_max = min(sbac_config.CLAIM_SCORE_MAX, sao.claim_1_score + 20)
    sao.claim_1_perf_lvl = _pick_performance_level(sao.claim_1_score, claim_cut_points)

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
