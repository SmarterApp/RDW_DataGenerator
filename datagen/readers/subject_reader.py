"""
A reader for subject XML files.

"""

import glob
from distutils.util import strtobool
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from datagen.generators.subject import set_custom_defaults
from datagen.model.scorable import Scorable
from datagen.model.subject import Subject, SubjectAssessmentType, SubjectScoring


def load_subjects(glob_pattern: str):
    """
    Load subjects from matching files

    :param glob_pattern: file pattern to match and load
    :return: loaded subjects
    """
    subjects = []
    for file in (glob.glob(glob_pattern)):
        subject = load_subject_file(file)
        if subject:
            # ?should we be calling this here or should the caller have to do that?
            set_custom_defaults(subject)
            subjects.append(subject)
    return subjects


def load_subject_file(file: str):
    """
    Load subject from a file

    :param file: filename
    :return: subject
    """

    tree = ElementTree.parse(file)
    root = tree.getroot()

    subject = Subject(root.get('code'))

    types = root.find('./AssessmentTypes')
    if types:
        for type in types:
            code = type.get('code').upper()
            assessment_type = SubjectAssessmentType(code)
            assessment_type.overall_scoring = __extract_scoring(type.find('./OverallScoring'))
            assessment_type.alt_scoring = __extract_scoring(type.find('./AltScoring'))
            assessment_type.claim_scoring = __extract_scoring(type.find('./ClaimScoring'))
            subject.types[code] = assessment_type

    altscores = root.find('./AltScores')
    if altscores:
        for altscore in altscores:
            if not subject.alts:
                subject.alts = []
            subject.alts.append(Scorable(altscore.get('code'), altscore.get('name')))

    claims = root.find('./Claims')
    if claims:
        for claim in claims:
            if not strtobool(claim.get('scorable', 'true')):
                continue
            if not subject.claims:
                subject.claims = []
            subject.claims.append(Scorable(claim.get('code'), claim.get('name')))

    return subject


def __extract_scoring(element: Element):
    if element:
        levels = element.findall('.//PerformanceLevel')
        return SubjectScoring(len(levels), min_score = element.get('minScore'), max_score = element.get('maxScore'))
    return None
