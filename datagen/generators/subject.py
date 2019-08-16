"""
Generate default subjects
"""
from datagen.model.scorable import Scorable
from datagen.model.subject import Subject

CLAIM_DEFINITIONS = {'Math': [{'code': '1', 'name': 'Concepts & Procedures', 'weight': .4},
                              {'code': 'SOCK_2', 'name': 'Problem Solving and Modeling & Data Analysis', 'weight': .45},
                              {'code': '3', 'name': 'Communicating Reasoning', 'weight': .15}],
                     'ELA': [{'code': 'SOCK_R', 'name': 'Reading', 'weight': .20},
                             {'code': '2-W', 'name': 'Writing', 'weight': .25},
                             {'code': 'SOCK_LS', 'name': 'Listening', 'weight': .25},
                             {'code': '4-CR', 'name': 'Research & Inquiry', 'weight': .30}]
                     }


def generate_default_subjects() -> [Subject]:
    return [__generate_math(), __generate_ela()]


def __generate_math() -> Subject:
    subject = Subject('Math')
    subject.types = ['SUM', 'ICA', 'IAB']
    subject.overall = Scorable('Overall', 'Overall', 1000, 3500)
    subject.claims = [Scorable(claim_def['code'], claim_def['name']) for claim_def in CLAIM_DEFINITIONS['Math']]
    set_custom_defaults(subject)
    return subject


def __generate_ela() -> Subject:
    subject = Subject('ELA')
    subject.types = ['SUM', 'ICA', 'IAB']
    subject.overall = Scorable('Overall', 'Overall', 1000, 3500)
    subject.claims = [Scorable(claim_def['code'], claim_def['name']) for claim_def in CLAIM_DEFINITIONS['ELA']]
    set_custom_defaults(subject)
    return subject


def set_custom_defaults(subject: Subject):
    """ Given a subject, set custom default values to make up for missing configuration data.
    This is a separate method because it needs to be applied to subjects that
    are loaded from subject definition files.

    :param subject: subject to modify
    """
    __set_default_claim_weights(subject)
    __set_default_alt_score_weights(subject)

    if subject.code == 'ELPAC':
        subject.emit_overall_stderr = False
        subject.emit_claim_score = False

    subject.sbac_claim_levels = subject.code in ['Math', 'ELA', 'ELPAC']
    subject.el_adjacent = get_el_adjacent(subject.code)


def get_el_adjacent(subject_code: str):
    return subject_code in ['ELA', 'ELPAC']


def __set_default_alt_score_weights(subject: Subject):
    if subject.alts:
        for alt in subject.alts:
            alt.weight = 1.0 / len(subject.alts)


def __set_default_claim_weights(subject: Subject):
    """ Given a subject, set the claim scoring weights (in place) to the default values

    :param subject: subject with claims to modify
    """
    if subject.claims and subject.code in CLAIM_DEFINITIONS:
        claim_defs = CLAIM_DEFINITIONS[subject.code]
        for claim in subject.claims:
            for claim_def in claim_defs:
                if claim_def['code'] == claim.code:
                    claim.weight = claim_def['weight']
                    break
    elif subject.claims:
        for claim in subject.claims:
            claim.weight = 1.0 / len(subject.claims)
