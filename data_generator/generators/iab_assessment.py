"""
An assessment generator
"""

import datetime

import data_generator.config.cfg as cfg
import data_generator.generators.assessment as gen_asmt_generator
from data_generator.model.assessment import Assessment
from data_generator.model.claim import Claim
from data_generator.model.claimscore import ClaimScore
from data_generator.model.interimassessment import InterimAssessment
from data_generator.model.interimassessmentoutcome import InterimAssessmentOutcome
from data_generator.model.student import Student
from data_generator.util.assessment_stats import random_stderr, claim_perf_lvl, score_given_capability
from data_generator.util.id_gen import IDGen


def create_iab_outcome_object(date_taken: datetime.date,
                              student: Student,
                              iab_asmt: InterimAssessment,
                              id_gen: IDGen,
                              iab_results: {str: InterimAssessmentOutcome},
                              gen_item=True):
    """

    :param date_taken:
    :param student:
    :param iab_asmt:
    :param id_gen:
    :param iab_results:
    :param gen_item:
    :return:
    """
    # Make sure the assessment is known in the results
    if iab_asmt.guid not in iab_results:
        iab_results[iab_asmt.guid] = []

    # Create the original outcome object
    ao = generate_interim_assessment_outcome(date_taken, student, iab_asmt, id_gen, gen_item=gen_item)
    iab_results[iab_asmt.guid].append(ao)


def generate_interim_assessment(asmt_year: int,
                                subject: str,
                                block: str,
                                grade: int,
                                id_gen: IDGen,
                                gen_item=True):
    """
    Generate an assessment object.

    @param asmt_year: Assessment year
    @param subject: Assessment subject
    @param block: block
    @param grade: grade
    @param id_gen: id generator
    @param gen_item: If should create item-level item bank
    @returns: The assessment object
    """
    asmt_scale_scores = cfg.ASMT_SCALE_SCORE[subject][grade]

    # Run the General generator
    sa = gen_asmt_generator.generate_assessment(Assessment)

    # Set other specifics based on SmarterBalanced conventions
    sa.rec_id = id_gen.get_rec_id('assessment')
    sa.type = 'INTERIM ASSESSMENT BLOCK'
    sa.year = asmt_year
    sa.version = cfg.ASMT_VERSION
    sa.name = 'SBAC-IAB-FIXED-G{}{}-{}-{}-{}'.format(grade, subject[0], ''.join(c for c in block if c.isupper()), subject, grade)
    sa.id = '(SBAC){}-{}-{}'.format(sa.name, asmt_year-1, asmt_year)
    sa.subject = subject
    sa.grade = grade
    sa.bank_key = '200'
    sa.perf_lvl_name_1 = cfg.CLAIM_PERF_LEVEL_NAME_1
    sa.perf_lvl_name_2 = cfg.CLAIM_PERF_LEVEL_NAME_2
    sa.perf_lvl_name_3 = cfg.CLAIM_PERF_LEVEL_NAME_3
    sa.perf_lvl_name_4 = None
    sa.perf_lvl_name_5 = None
    sa.overall_score_min = asmt_scale_scores[0]
    sa.overall_score_max = asmt_scale_scores[-1]
    sa.claim_perf_lvl_name_1 = cfg.CLAIM_PERF_LEVEL_NAME_1
    sa.claim_perf_lvl_name_2 = cfg.CLAIM_PERF_LEVEL_NAME_2
    sa.claim_perf_lvl_name_3 = cfg.CLAIM_PERF_LEVEL_NAME_3
    sa.overall_cut_point_1 = asmt_scale_scores[1]
    sa.overall_cut_point_2 = asmt_scale_scores[2]
    sa.overall_cut_point_3 = asmt_scale_scores[3]
    # IABs don't really have claims (because they are like a claim) but there is code that expects claim_1 to exist
    sa.claims = [Claim(block, block, asmt_scale_scores[0], asmt_scale_scores[-1])]
    sa.effective_date = datetime.date(asmt_year-1, 8, 15)
    sa.from_date = sa.effective_date
    sa.to_date = cfg.ASMT_TO_DATE
    gen_asmt_generator.generate_segment_and_item_bank(sa, gen_item, cfg.IAB_ITEM_BANK_SIZE, id_gen)

    return sa


def generate_interim_assessment_outcome(date_taken: datetime.date,
                                        student: Student,
                                        assessment: Assessment,
                                        id_gen: IDGen,
                                        gen_item=True):
    """
    Generate an assessment outcome for a given student.

    @param date_taken: date test was taken
    @param student: The student to create the outcome for
    @param assessment: The assessment to create the outcome for
    @param id_gen: ID generator
    @param gen_item: If should create item-level responses
    @returns: The assessment outcome
    """

    # Run the General generator
    sao = gen_asmt_generator.generate_assessment_outcome(student, assessment, id_gen)

    # Set other specifics
    sao.school = student.school
    sao.date_taken = date_taken
    sao.admin_condition = 'NS'
    gen_asmt_generator.generate_session(sao)

    # Generate assessment outcome Item-level data
    if gen_item: gen_asmt_generator.generate_item_data(sao)

    # set timestamps for the opportunity
    gen_asmt_generator.set_opportunity_dates(sao)

    # use the student capability to generate an overall score (level for IABs is calculated differently, see below)
    sao.overall_score, level = score_given_capability(student.capability[assessment.subject], assessment.get_cuts())

    # now that we have a score, generate a random SE and figure out IAB perf level (1-3) using SB formulae
    stderr = random_stderr(sao.overall_score, assessment.overall_score_min, assessment.overall_score_max)
    sao.overall_score_stderr = stderr
    sao.overall_score_range_min = max(assessment.overall_score_min, sao.overall_score - stderr)
    sao.overall_score_range_max = min(assessment.overall_score_max, sao.overall_score + stderr)
    sao.overall_perf_lvl = claim_perf_lvl(sao.overall_score, stderr, assessment.overall_cut_point_2)

    # The legacy output expects there to be a claim_1_score; not really correct for IABs but for now ...
    sao.claim_scores = [ClaimScore(assessment.claims[0], sao.overall_score, sao.overall_score_stderr,
                                   sao.overall_perf_lvl, sao.overall_score_range_min, sao.overall_score_range_max)]

    return sao
