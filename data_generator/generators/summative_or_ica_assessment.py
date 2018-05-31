"""
An assessment generator for the SBAC assessment.

"""

import datetime
import random

import data_generator.config.cfg as cfg
import data_generator.generators.assessment as gen_asmt_generator
from data_generator.model.assessment import Assessment
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.student import Student
from data_generator.util.assessment_stats import random_claim_error, claim_perf_lvl, \
    score_given_capability, perf_level_given_capability
from data_generator.util.assessment_stats import random_claims
from data_generator.util.id_gen import IDGen


def create_assessment_outcome_object(date_taken: datetime.date,
                                     student: Student,
                                     asmt: Assessment,
                                     id_gen: IDGen,
                                     assessment_results: {str: AssessmentOutcome},
                                     skip_rate=cfg.ASMT_SKIP_RATE,
                                     retake_rate=cfg.ASMT_RETAKE_RATE,
                                     delete_rate=cfg.ASMT_DELETE_RATE,
                                     update_rate=cfg.ASMT_UPDATE_RATE,
                                     gen_item=True):
    """
    Create the outcome(s) for a single assessment for a student. If the student is determined to have skipped the
    assessment, the resulting array will be empty. Otherwise, one outcome will be created with the chance that a second
    outcome is also created. A second outcome will be created if the assessment is re-taken or updated. If the
    assessment is determined to have been deleted, no second record will be created.

    @param date_taken: date taken
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
    if asmt.guid not in assessment_results:
        assessment_results[asmt.guid] = []

    # Create the original outcome object
    ao = generate_assessment_outcome(date_taken, student, asmt, id_gen, gen_item=gen_item)
    assessment_results[asmt.guid].append(ao)

    # Decide if something special is happening
    special_random = random.random()
    if special_random < retake_rate:
        # Set the original outcome object to inactive, create a new outcome (with an advanced date take), and return
        ao.result_status = cfg.ASMT_STATUS_INACTIVE
        ao2 = generate_assessment_outcome(date_taken + datetime.timedelta(days=7), student, asmt, id_gen, gen_item=gen_item)
        assessment_results[asmt.guid].append(ao2)
    elif special_random < update_rate:
        # Set the original outcome object to deleted and create a new outcome
        ao.result_status = cfg.ASMT_STATUS_DELETED
        ao2 = generate_assessment_outcome(date_taken, student, asmt, id_gen, gen_item=gen_item)
        assessment_results[asmt.guid].append(ao2)

        # See if the updated record should be deleted
        if random.random() < delete_rate:
            ao2.result_status = cfg.ASMT_STATUS_DELETED
    elif special_random < delete_rate:
        # Set the original outcome object to deleted
        ao.result_status = cfg.ASMT_STATUS_DELETED


def generate_assessment(type, asmt_year, subject, grade, id_gen, from_date=None, to_date=None,
                        claim_definitions=cfg.CLAIM_DEFINITIONS, gen_item=True):
    """
    Generate an assessment object.

    @param type: Assessment type
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
    asmt_scale_scores = cfg.ASMT_SCALE_SCORE[subject][grade]

    # Run the General generator
    sa = gen_asmt_generator.generate_assessment(Assessment)

    # Set other specifics based on SmarterBalanced conventions
    sa.name = 'SBAC-{}-{}'.format(subject, grade)
    sa.id = '(SBAC){}-{}-{}-{}'.format(sa.name, 'Spring' if type == 'SUMMATIVE' else 'Winter', asmt_year-1, asmt_year)
    sa.subject = subject
    sa.grade = grade
    sa.rec_id = id_gen.get_rec_id('assessment')
    sa.type = type
    sa.year = asmt_year
    sa.version = cfg.ASMT_VERSION
    sa.subject = subject
    sa.bank_key = '200'
    sa.claim_1_name = claims[0]['name']
    sa.claim_2_name = claims[1]['name']
    sa.claim_3_name = claims[2]['name']
    sa.claim_4_name = claims[3]['name'] if len(claims) == 4 else None
    sa.perf_lvl_name_1 = cfg.ASMT_PERF_LEVEL_NAME_1
    sa.perf_lvl_name_2 = cfg.ASMT_PERF_LEVEL_NAME_2
    sa.perf_lvl_name_3 = cfg.ASMT_PERF_LEVEL_NAME_3
    sa.perf_lvl_name_4 = cfg.ASMT_PERF_LEVEL_NAME_4
    sa.perf_lvl_name_5 = cfg.ASMT_PERF_LEVEL_NAME_5
    sa.overall_score_min = asmt_scale_scores[0]
    sa.overall_score_max = asmt_scale_scores[-1]
    sa.claim_1_score_min = asmt_scale_scores[0]
    sa.claim_1_score_max = asmt_scale_scores[-1]
    sa.claim_1_score_weight = claims[0]['weight']
    sa.claim_2_score_min = asmt_scale_scores[0]
    sa.claim_2_score_max = asmt_scale_scores[-1]
    sa.claim_2_score_weight = claims[1]['weight']
    sa.claim_3_score_min = asmt_scale_scores[0]
    sa.claim_3_score_max = asmt_scale_scores[-1]
    sa.claim_3_score_weight = claims[2]['weight']
    sa.claim_4_score_min = asmt_scale_scores[0] if len(claims) == 4 else None
    sa.claim_4_score_max = asmt_scale_scores[-1] if len(claims) == 4 else None
    sa.claim_4_score_weight = claims[3]['weight'] if len(claims) == 4 else None
    sa.claim_perf_lvl_name_1 = cfg.CLAIM_PERF_LEVEL_NAME_1
    sa.claim_perf_lvl_name_2 = cfg.CLAIM_PERF_LEVEL_NAME_2
    sa.claim_perf_lvl_name_3 = cfg.CLAIM_PERF_LEVEL_NAME_3
    sa.overall_cut_point_1 = asmt_scale_scores[1]
    sa.overall_cut_point_2 = asmt_scale_scores[2]
    sa.overall_cut_point_3 = asmt_scale_scores[3]
    sa.effective_date = datetime.date(asmt_year - 1, 8, 15)
    sa.from_date = from_date if from_date is not None else sa.effective_date
    sa.to_date = to_date if to_date is not None else cfg.ASMT_TO_DATE
    gen_asmt_generator.generate_segment_and_item_bank(sa, gen_item, cfg.ASMT_ITEM_BANK_SIZE, id_gen)

    return sa


def generate_assessment_outcome(date_taken: datetime.date,
                                student: Student,
                                assessment: Assessment,
                                id_gen,
                                gen_item=True):
    """
    Generate an assessment outcome for a given student.

    @param date_taken: date taken
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
    sao.admin_condition = 'Valid' if assessment.type == 'SUMMATIVE' else 'SD'
    sao.date_taken = date_taken
    gen_asmt_generator.generate_session(sao)

    # Generate assessment outcome Item-level data
    if gen_item: gen_asmt_generator.generate_item_data(sao)

    # set timestamps for the opportunity
    gen_asmt_generator.set_opportunity_dates(sao)

    # use the student capability to generate an overall score and performance level
    sao.overall_score = score_given_capability(student.capability[assessment.subject],
        [assessment.overall_score_min, assessment.overall_cut_point_1, assessment.overall_cut_point_2, assessment.overall_cut_point_3, assessment.overall_score_max])
    sao.overall_perf_lvl = perf_level_given_capability(student.capability[assessment.subject])

    overall_range_min = random.randint(50, 100)  # Total score range is between 100 and 200 points around score
    overall_range_max = random.randint(50, 100)  # Total score range is between 100 and 200 points around score
    sao.overall_score_range_min = max(assessment.overall_score_min, sao.overall_score - overall_range_min)
    sao.overall_score_range_max = min(assessment.overall_score_max, sao.overall_score + overall_range_max)

    claims = cfg.CLAIM_DEFINITIONS[assessment.subject]
    claim_weights = [claim['weight'] for claim in claims]
    claim_scores = random_claims(sao.overall_score, claim_weights, assessment.overall_score_min, assessment.overall_score_max)

    sao.claim_1_score = claim_scores[0]
    stderr = random_claim_error(sao.claim_1_score, assessment.overall_score_min, assessment.overall_score_max)
    sao.claim_1_score_range_min = max(assessment.claim_1_score_min, sao.claim_1_score - stderr)
    sao.claim_1_score_range_max = min(assessment.claim_1_score_max, sao.claim_1_score + stderr)
    sao.claim_1_perf_lvl = claim_perf_lvl(sao.claim_1_score, stderr, assessment.overall_cut_point_2)

    sao.claim_2_score = claim_scores[1]
    stderr = random_claim_error(sao.claim_2_score, assessment.overall_score_min, assessment.overall_score_max)
    sao.claim_2_score_range_min = max(assessment.claim_2_score_min, sao.claim_2_score - stderr)
    sao.claim_2_score_range_max = min(assessment.claim_2_score_max, sao.claim_2_score + stderr)
    sao.claim_2_perf_lvl = claim_perf_lvl(sao.claim_2_score, stderr, assessment.overall_cut_point_2)

    sao.claim_3_score = claim_scores[2]
    stderr = random_claim_error(sao.claim_3_score, assessment.overall_score_min, assessment.overall_score_max)
    sao.claim_3_score_range_min = max(assessment.claim_3_score_min, sao.claim_3_score - stderr)
    sao.claim_3_score_range_max = min(assessment.claim_3_score_max, sao.claim_3_score + stderr)
    sao.claim_3_perf_lvl = claim_perf_lvl(sao.claim_3_score, stderr, assessment.overall_cut_point_2)

    if assessment.claim_4_name is not None:
        if len(claim_scores) != 4:
            raise Exception(
                "unexpected number of claim scores: %s %s %s" % (assessment.subject, claim_scores, claim_weights))

        sao.claim_4_score = claim_scores[3]
        stderr = random_claim_error(sao.claim_4_score, assessment.overall_score_min, assessment.overall_score_max)
        sao.claim_4_score_range_min = max(assessment.claim_4_score_min, sao.claim_4_score - stderr)
        sao.claim_4_score_range_max = min(assessment.claim_4_score_max, sao.claim_4_score + stderr)
        sao.claim_4_perf_lvl = claim_perf_lvl(sao.claim_4_score, stderr, assessment.overall_cut_point_2)

    elif len(claim_scores) != 3:
        raise Exception(
            "unexpected number of claim scores: %s %s %s" % (assessment.subject, claim_scores, claim_weights))

    return sao
