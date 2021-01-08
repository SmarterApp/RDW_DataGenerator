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
from datagen.model.score import Score
from datagen.model.student import Student
from datagen.model.targetscore import TargetScore
from datagen.util.assessment_stats import random_subscores, performance_level, even_cuts
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
    sao.admin_condition = 'Valid' if assessment.is_summative() else 'SD'
    sao.date_taken = date_taken
    gen_asmt_generator.generate_session(sao)

    # Generate assessment outcome Item-level data
    if gen_item:
        gen_asmt_generator.generate_item_data(sao)

    # set timestamps for the opportunity
    gen_asmt_generator.set_opportunity_dates(sao)

    # use the student capability to generate an overall score and performance level
    overall = Score('Overall')
    overall.score, overall.perf_lvl = score_given_capability(student.capability[assessment.subject.code], assessment.overall.get_cuts())
    overall.stderr = random_stderr(overall.score, assessment.overall.score_min, assessment.overall.score_max) if assessment.subject.emit_overall_stderr else None
    sao.overall = overall

    _generate_alt_scores(sao, assessment, overall)
    _generate_claim_scores(sao, assessment, overall)
    _generate_trait_scores(sao, assessment, student)
    _generate_target_scores(sao, assessment, student)

    return sao


def _generate_alt_scores(sao: AssessmentOutcome, assessment: Assessment, overall: Score):
    """Modify the assessment outcome to add alt scores if indicated.
    Note that we're using the overall min/max scores; some day we should use alt-specific values.

    :param sao: AssessmentOutcome to enhance with alt scores
    :param assessment: assessment
    :param overall: overall score
    """
    if assessment.alts and len(assessment.alts) > 0:
        sao.alt_scores = []
        alt_weights = [alt_def.weight for alt_def in assessment.alts]
        alt_scores = random_subscores(overall.score, alt_weights, assessment.overall.score_min, assessment.overall.score_max)
        for alt, alt_score in zip(assessment.alts, alt_scores):
            sao.alt_scores.append(
                Score(alt.code, alt_score,
                      random_stderr(alt_score, assessment.overall.score_min, assessment.overall.score_max),
                      performance_level(alt_score, alt.get_cuts())))


def _generate_claim_scores(sao: AssessmentOutcome, assessment: Assessment, overall: Score):
    """Modify the assessment outcome to add claim scores if indicated.

    :param sao: AssessmentOutcome to enhance with alt scores
    :param assessment: assessment
    :param overall: overall score
    """
    if assessment.claims and len(assessment.claims) > 0:
        # use the overall min/max score for claims (since we don't have any other values to use)
        min_score = assessment.overall.score_min
        max_score = assessment.overall.score_max

        claim_weights = [claim_def.weight for claim_def in assessment.claims]
        claim_scores = random_subscores(overall.score, claim_weights, min_score, max_score)

        # non-SB claims need cut-points to calculate their level; we don't have information on
        # that so just assume an even distribution between min/max values.
        # We need to get the number of claim performance levels from the subject definition.
        levels = assessment.subject.types[assessment.type].claim_scoring.perf_levels
        claim_cuts = even_cuts(min_score, max_score, levels)

        sao.claim_scores = []
        for claim, claim_score in zip(assessment.claims, claim_scores):
            stderr = random_stderr(claim_score, min_score, max_score)
            claim_level = claim_perf_lvl(claim_score, stderr, assessment.overall.cut_points[1]) \
                if assessment.subject.sbac_claim_levels else performance_level(claim_score, claim_cuts)
            sao.claim_scores.append(Score(claim.code, claim_score, stderr, claim_level)
                                    if assessment.subject.emit_claim_score else Score(claim.code, None, None, claim_level))


def _generate_trait_scores(sao: AssessmentOutcome, assessment: Assessment, student: Student):
    """Modify the assessment outcome to add trait scores if indicated.
    Note: if this is a legacy SmarterBalanced assessment with WER items, there may be a WER item
    with subscores already generated. We were using these item subscores here at the exam level, but
    now we will generate new exam-level trait scores regardless.

    :param sao: AssessmentOutcome to enhance with alt scores
    :param assessment: assessment
    :param overall: overall score
    """
    if assessment.is_summative() and assessment.subject.traits:
        # List of possible condition codes to use when score is 0
        condition_codes = ['B', 'L', 'I', 'M', 'T']

        # randomly select a purpose (simulates CAT giving students different questions)
        purpose = random.choice(assessment.subject.traits).purpose

        sao.trait_scores = []
        for trait in (trait for trait in assessment.subject.traits if trait.purpose == purpose):
            score = int((trait.max_score + 1) * student.capability[assessment.subject.code] / 4.0)
            condition_code = '' if score != 0 else random.choice(condition_codes)
            sao.trait_scores.append(Score(trait.code, score, condition_code=condition_code))


def _generate_target_scores(sao: AssessmentOutcome, assessment: Assessment, student: Student):
    """Modify the assessment outcome to add target scores if indicated.
    NOTE: these are really fake values, with no real correlation to overall/item scores:
     * student_residual - since everything is generated uniformly, this should be really close to 0
     * standard_met_residual - this is based on student capability so offset uniform distribution

    :param sao: AssessmentOutcome to enhance with alt scores
    :param assessment: assessment
    :param overall: overall score
    """
    # for summative assessments, if the items have target information, generate target residuals
    if assessment.is_summative() and assessment.item_bank and any(item.target for item in assessment.item_bank):
        # collect the unique targets from all items
        targets = Counter(item.target for item in assessment.item_bank if item.target)
        offset = (student.capability[assessment.subject.code] - 2.0) / 2.0
        sao.target_scores = [TargetScore(t, random.uniform(-0.1, +0.1), random.triangular(-1.0, +1.0, offset))
                             for t in targets.keys()]
