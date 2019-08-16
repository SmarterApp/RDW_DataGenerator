"""
A reader for subject XML files.

"""

import glob
from distutils.util import strtobool
from xml.etree import ElementTree

from datagen.generators.subject import set_custom_defaults
from datagen.model.scorable import Scorable
from datagen.model.subject import Subject


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
            code = type.get('code')
            subject.types.append(code.upper())

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
