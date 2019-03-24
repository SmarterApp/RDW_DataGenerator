"""

"""
import pytest

from datagen.util.assessment_stats import DemographicLevels, Stats, score_given_capability, performance_level
from datagen.util.assessment_stats import RandomLevelByDemographics, Properties, GradeLevels
from datagen.util.assessment_stats import random_capability
from datagen.util.weighted_choice import weighted_choice


def gen_random_entity(demographics):
    return {demo_name: weighted_choice(distribution)
            for demo_name, distribution in demographics.items()}


def test_random_level():
    """

    """
    demographics = Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 0.0},
    )

    level_breakdowns = \
        GradeLevels((14.0, 30.0, 49.0, 7.0),
                    dmg_prg_504=DemographicLevels({True: Stats(45.0, 37.0, 17.0, 1.0),
                                                   False: Stats(11.304347826086957, 29.391304347826086,
                                                                51.78260869565217, 7.521739130434782)}),
                    dmg_prg_tt1=DemographicLevels({True: Stats(20.0, 38.0, 39.0, 3.0),
                                                   False: Stats(6.363636363636363, 19.818181818181817,
                                                                61.72727272727273, 12.090909090909092)}),
                    dmg_prg_iep=DemographicLevels({True: Stats(45.0, 37.0, 17.0, 1.0),
                                                   False: Stats(8.529411764705882, 28.764705882352942,
                                                                54.64705882352941, 8.058823529411764)}),
                    dmg_prg_lep=DemographicLevels({True: Stats(38.0, 43.0, 19.0, 0.0),
                                                   False: Stats(11.626373626373626, 28.714285714285715,
                                                                51.967032967032964,
                                                                7.6923076923076925)}),
                    gender=DemographicLevels(female=Stats(11.0, 29.0, 52.0, 8.0),
                                             male=Stats(16.0, 33.0, 46.0, 5.0),
                                             not_stated=Stats(9.0, 30.0, 51.0, 10.0)),
                    race=DemographicLevels(dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                                           dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                                           dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                                           dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                                           dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                                           dmg_eth_pcf=Stats(0.0, 0.0, 0.0, 0.0),
                                           dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0)))

    level_generator = RandomLevelByDemographics(demographics, level_breakdowns)

    for _ in range(10000):
        entity = gen_random_entity(demographics)
        level = level_generator.random_level(entity)


def test_random_capability():
    avg = 0
    for _ in range(0, 100):
        value = random_capability([0.04, 0.32, 0.57, 0.07])
        assert 0 <= value < 4.0
        avg += value
    avg /= 100.0
    assert 1.5 < avg < 3.0  # should be 2.17


def test_random_capability_with_negative_adj():
    avg = 0
    for _ in range(0, 100):
        value = random_capability([0.04, 0.32, 0.57, 0.07], -0.6)
        assert 0 <= value < 4.0
        avg += value
    avg /= 100.0
    assert 1.0 < avg < 2.0  # should be 1.5


def test_random_capability_with_positive_adj():
    avg = 0
    for _ in range(0, 100):
        value = random_capability([0.04, 0.32, 0.57, 0.07], 0.5)
        assert 0 <= value < 4.0
        avg += value
    avg /= 100.0
    assert 2.0 < avg < 3.5  # should be 2.9


def test_performance_level():
    assert 1 == performance_level(1150.0, [1150, 1480, 1526, 1575, 1900, 1900])
    assert 1 == performance_level(1400.0, [1150, 1480, 1526, 1575, 1900, 1900])
    assert 2 == performance_level(1480.0, [1150, 1480, 1526, 1575, 1900, 1900])
    assert 2 == performance_level(1500.0, [1150, 1480, 1526, 1575, 1900, 1900])
    assert 3 == performance_level(1526.0, [1150, 1480, 1526, 1575, 1900, 1900])
    assert 3 == performance_level(1550.0, [1150, 1480, 1526, 1575, 1900, 1900])
    assert 4 == performance_level(1575.0, [1150, 1480, 1526, 1575, 1900, 1900])
    assert 4 == performance_level(1600.0, [1150, 1480, 1526, 1575, 1900, 1900])
    assert 4 == performance_level(1900.0, [1150, 1480, 1526, 1575, 1900, 1900])


def test_performance_level_fails_for_low_score():
    with pytest.raises(ValueError) as e:
        performance_level(1100.0, [1150, 1480, 1526, 1575, 1900, 1900])


def test_performance_level_fails_for_high_score():
    with pytest.raises(ValueError) as e:
        performance_level(2100.0, [1150, 1480, 1526, 1575, 1900, 1900])


def _assert_score_given_capability(capability, cuts, mean_score, max_score_delta, mean_level, max_level_delta, cnt=20):
    total_score = 0
    total_level = 0
    for _ in range(0, cnt):
        score, level = score_given_capability(capability, cuts)
        # print(score, level)
        total_score += score
        total_level += level
    score = total_score / cnt
    level = total_level / cnt
    # print(score, level)
    assert 0 <= abs(score - mean_score) <= max_score_delta
    assert 0 <= abs(level - mean_level) <= max_level_delta


def test_score_given_capability_with_two_levels():
    _assert_score_given_capability(0.0, [2300, 2500, 2700], 2300, 25, 1.0, 0.3)
    _assert_score_given_capability(1.0, [2300, 2500, 2700], 2400, 25, 1.0, 0.4)
    _assert_score_given_capability(2.0, [2300, 2500, 2700], 2500, 25, 1.5, 0.4)
    _assert_score_given_capability(3.0, [2300, 2500, 2700], 2600, 25, 2.0, 0.4)
    _assert_score_given_capability(3.99, [2300, 2500, 2700], 2699, 25, 2.0, 0.3)


def test_score_given_capability_with_six_levels():
    _assert_score_given_capability(0.0, [2300, 2400, 2500, 2600, 2700, 2800, 2900], 2300, 15, 1.0, 0.3)
    _assert_score_given_capability(1.0, [2300, 2400, 2500, 2600, 2700, 2800, 2900], 2450, 15, 2.0, 0.3)
    _assert_score_given_capability(2.0, [2300, 2400, 2500, 2600, 2700, 2800, 2900], 2600, 15, 3.5, 0.3)
    _assert_score_given_capability(3.0, [2300, 2400, 2500, 2600, 2700, 2800, 2900], 2750, 15, 5.0, 0.3)
    _assert_score_given_capability(3.99, [2300, 2400, 2500, 2600, 2700, 2800, 2900], 2899, 15, 6.0, 0.3)
