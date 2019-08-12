"""
An assessment generator
"""

import datetime

import datagen.generators.assessment as gen_asmt_generator
from datagen.model.assessment import Assessment
from datagen.model.assessmentoutcome import AssessmentOutcome
from datagen.model.score import Score
from datagen.model.student import Student
from datagen.util.assessment_stats import random_stderr, claim_perf_lvl, score_given_capability
from datagen.util.id_gen import IDGen


def create_iab_outcome_object(date_taken: datetime.date,
                              student: Student,
                              iab_asmt: Assessment,
                              id_gen: IDGen,
                              iab_results: {str: AssessmentOutcome},
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

    # use the student capability to generate an overall score
    # note that IAB level is calculated differently using SB formulae
    overall = Score('Overall')
    overall.score, level = \
        score_given_capability(student.capability[assessment.subject_code], assessment.overall.get_cuts())
    overall.stderr = random_stderr(overall.score, assessment.overall.score_min, assessment.overall.score_max)
    overall.perf_lvl = claim_perf_lvl(overall.score, overall.stderr, assessment.overall.cut_points[1])
    sao.overall = overall

    return sao
