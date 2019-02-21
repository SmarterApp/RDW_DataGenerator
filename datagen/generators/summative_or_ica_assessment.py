"""
An assessment generator for the SBAC assessment.

"""

import datetime
import random
from collections import Counter

import datagen.config.cfg as cfg
import datagen.generators.assessment as gen_asmt_generator
from datagen.model.assessment import Assessment
from datagen.model.assessmentoutcome import AssessmentOutcome
from datagen.model.claim import Claim
from datagen.model.claimscore import ClaimScore
from datagen.model.student import Student
from datagen.model.targetscore import TargetScore
from datagen.util.assessment_stats import random_claims
from datagen.util.assessment_stats import random_stderr, claim_perf_lvl, score_given_capability
from datagen.util.id_gen import IDGen


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
        ao2 = generate_assessment_outcome(
            date_taken + datetime.timedelta(days=7), student, asmt, id_gen, gen_item=gen_item)
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
    # generated ICA/Summative assessments have 4 performance levels
    sa.perf_lvl_name_1 = cfg.ASMT_PERF_LEVEL_NAME_1
    sa.perf_lvl_name_2 = cfg.ASMT_PERF_LEVEL_NAME_2
    sa.perf_lvl_name_3 = cfg.ASMT_PERF_LEVEL_NAME_3
    sa.perf_lvl_name_4 = cfg.ASMT_PERF_LEVEL_NAME_4
    sa.overall_score_min = asmt_scale_scores[0]
    sa.overall_score_max = asmt_scale_scores[4]
    sa.overall_cut_point_1 = asmt_scale_scores[1]
    sa.overall_cut_point_2 = asmt_scale_scores[2]
    sa.overall_cut_point_3 = asmt_scale_scores[3]
    sa.claim_perf_lvl_name_1 = cfg.CLAIM_PERF_LEVEL_NAME_1
    sa.claim_perf_lvl_name_2 = cfg.CLAIM_PERF_LEVEL_NAME_2
    sa.claim_perf_lvl_name_3 = cfg.CLAIM_PERF_LEVEL_NAME_3
    sa.claims = [Claim(claim['code'], claim['name'], asmt_scale_scores[0], asmt_scale_scores[-1]) for claim in claims]
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
    if gen_item:
        gen_asmt_generator.generate_item_data(sao)

    # set timestamps for the opportunity
    gen_asmt_generator.set_opportunity_dates(sao)

    # use the student capability to generate an overall score and performance level
    sao.overall_score, sao.overall_perf_lvl = \
        score_given_capability(student.capability[assessment.subject], assessment.get_cuts())

    stderr = random_stderr(sao.overall_score, assessment.overall_score_min, assessment.overall_score_max)
    sao.overall_score_stderr = stderr
    sao.overall_score_range_min = max(assessment.overall_score_min, sao.overall_score - stderr)
    sao.overall_score_range_max = min(assessment.overall_score_max, sao.overall_score + stderr)

    # use (arbitrary) claim weights to generate claim scores
    # hack for custom subjects: give all claims equal weight
    claim_weights = [claim['weight'] for claim in cfg.CLAIM_DEFINITIONS[assessment.subject]] \
        if assessment.subject in cfg.CLAIM_DEFINITIONS else [1.0 / len(assessment.claims)] * len(assessment.claims)
    claim_scores = random_claims(
        sao.overall_score, claim_weights, assessment.overall_score_min, assessment.overall_score_max)
    sao.claim_scores = []
    for claim, claim_score in zip(assessment.claims, claim_scores):
        stderr = random_stderr(claim_score, assessment.overall_score_min, assessment.overall_score_max)
        # SmarterBalanced claim levels are very different, based on +-1.5 stderr
        claim_level = claim_perf_lvl(claim_score, stderr, assessment.overall_cut_point_2) \
            if assessment.subject in cfg.SUBJECTS \
            else [i for (i, cut) in enumerate(assessment.get_cuts()) if claim_score <= cut][0]
        sao.claim_scores.append(ClaimScore(claim, claim_score, stderr, claim_level,
                                           max(claim.score_min, claim_score - stderr),
                                           min(claim.score_max, claim_score + stderr)))

    # for summative assessments, if the items have target information, generate target residuals
    # NOTE: these are really fake values, with no real correlation to overall/item scores:
    #   student_residual - since everything is generated uniformly, this should be really close to 0
    #   standard_met_residual - this is based on student capability so offset uniform distribution
    if assessment.is_summative() and assessment.item_bank and any(item.target for item in assessment.item_bank):
        # collect the unique targets from all items
        targets = Counter(item.target for item in assessment.item_bank if item.target)
        offset = (student.capability[assessment.subject] - 2.0) / 2.0
        sao.target_scores = [TargetScore(t, random.uniform(-0.1, +0.1), random.triangular(-1.0, +1.0, offset))
                             for t in targets.keys()]

    return sao
