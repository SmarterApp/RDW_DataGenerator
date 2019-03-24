"""
An assessment generator
"""

import datetime

import datagen.generators.assessment as gen_asmt_generator
from datagen.model.assessment import Assessment
from datagen.model.claimscore import ClaimScore
from datagen.model.interimassessment import InterimAssessment
from datagen.model.interimassessmentoutcome import InterimAssessmentOutcome
from datagen.model.student import Student
from datagen.util.assessment_stats import random_stderr, claim_perf_lvl, score_given_capability
from datagen.util.id_gen import IDGen


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
    if gen_item:
        gen_asmt_generator.generate_item_data(sao)

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
