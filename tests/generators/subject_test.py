"""
Unit tests for the population module.

"""

from datagen.generators.subject import generate_default_subjects


def test_generate_default_subjects():
    subjects = generate_default_subjects()

    assert len(subjects) == 2

    math = subjects[0]
    assert math.code == 'Math'
    assert not math.alts
    assert len(math.claims) == 3
    assert [claim.weight for claim in math.claims] == [0.4, 0.45, 0.15]

    ela = subjects[1]
    assert ela.code == 'ELA'
    assert not ela.alts
    assert len(ela.claims) == 4
    assert [claim.weight for claim in ela.claims] == [0.2, 0.25, 0.25, 0.3]


if __name__ == '__main__':
    test_generate_default_subjects()




