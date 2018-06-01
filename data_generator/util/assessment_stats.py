# like sum, but with multiplication
import itertools
import math
import random
from functools import partial, reduce
from operator import mul

from data_generator.util.stats import normalize
from data_generator.util.weighted_choice import weighted_choice

product = partial(reduce, mul)


class Properties(dict):
    """ Wrapper for accessing a dict's values as attributes. """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class Stats:
    """ stats for a specific demographic value """

    def __init__(self, *values: [float]):
        self._values = normalize(values)

    def __getattr__(self, item):
        return getattr(self._values, item)

    def __getitem__(self, item):
        return self._values[item]


class DemographicLevels(dict):
    """ an individual demographic """

    def __init__(self, values: dict = None, **stats: {str: Stats}):
        super().__init__(**stats)
        if values is not None:
            self.update(values)


class GradeLevels(dict):
    """ dictionary of demographics by name """

    def __init__(self, totals: [float], **demographic_levels: {str: DemographicLevels}):
        super().__init__(**demographic_levels)
        self.totals = normalize(totals)

    @property
    def num_levels(self):
        """"""
        return len(self.totals)


class RandomLevelByDemographics:
    """
    We want to be able to generate assessment levels for a student in such a way that the distribution of
    the results matches our expectations for the distribution of levels for various demographics. Unfortunately,
    we only have data about the distribution of levels for individual demographics. However, We can use basic
    statistics to create a reasonable approximate distribution.

    By Bayes' law,

        P[student's score is a certain level | student demographics]

        = P[student demographics | student's score is a certain level]
          * P[student's score is a certain level]
          / P[student demographics]

    We make the simplifying assumption that the demographics are independent (the Naive Bayes assumption)

          P[demo1=val1 & demo2=val2 | level=X]
        = P[demo1=val1 | level=X) * P(demo2=val2 | level=X]

    This allows us to construct an approximate distribution, which we can use to choose a random level. In
    practice, this approximation seems to conform to the demographic distributions within a couple of percent.
    """

    def __init__(self,
                 demographics: dict,
                 level_breakdowns: GradeLevels):
        self.demographics = demographics
        self.level_breakdowns = level_breakdowns

    def _p_demo_is_val_given_level(self,
                                   demo_name: str,
                                   demo_val: str,
                                   level: int) -> float:
        """
          P(demo_name = demo_val | level)
        = P(level | demo_name = demo_val) / ( P(level | demo_name = val1) + P(level | demo_name = val2) + ... )
        """

        sum_ = sum(self.level_breakdowns[demo_name][demo_val2][level]
                   * self.demographics[demo_name][demo_val2]
                   for demo_val2 in self.demographics[demo_name])

        return self.level_breakdowns[demo_name][demo_val][level] * self.demographics[demo_name][demo_val] / sum_

    def _p_score_is_level(self, level: int) -> float:
        return self.level_breakdowns.totals[level]

    def _p_demo_is_val(self, demo_name: str, demo_val: str) -> float:
        return self.demographics[demo_name][demo_val]

    def distribution(self, entity: dict) -> [float]:
        """
        Generate a probability distribution for a student.

        The student is assumed to be a dict-like structure, where the keys are demographic names, and the
        values are the student's specific demographic group.

        @returns a list of floats, which sums to 1.
        """
        probs = [(self._p_score_is_level(level) *
                  product(self._p_demo_is_val_given_level(demo_name, demo_val, level)
                          for demo_name, demo_val in entity.items()))
                 for level in range(self.level_breakdowns.num_levels)]

        # normalize (instead of computing the denominator, which is fixed)
        return normalize(probs)

    def random_level(self,
                     entity: dict,
                     rng: random.Random = random.Random(),
                     seed=None) -> int:
        """
        Given a student, return a random level chosen according to their demographic values
        """
        probs = {i: prob for i, prob in enumerate(self.distribution(entity))}

        if all(prob == 0.0 for prob in probs.values()):
            # the demographics say this student doesn't exist...
            return rng.choice(list(probs.keys()))

        return weighted_choice(probs, rng=rng, seed=seed)


def random_capability(distribution: [float], adj: float = 0.0) -> float:
    """
    Given a distribution, e.g. [0.04,0.32,0.57,0.07] this will return the fractional level of a
    random value. The return will be 0-N where N is the number of values in the distribution.

    :param distribution: normalized distribution (i.e. adds up to 1)
    :param adj: optional capability adjustment (-1, +1) (gamma correction so negative reduces capability)
    :return: fractional value 0-N
    """
    # in theory this can be any size distribution but we know it is for performance levels so should be 4
    n = len(distribution)
    assert n == 4

    # accumulate values and stick a leading 0 in there
    values = [0.0] + list(itertools.accumulate(distribution))
    value = random.uniform(0, values[-1])
    for i in range(0, n):
        if value < values[i+1]:
            return adjust_capability(i + ((value - values[i]) / (values[i+1] - values[i])), adj)


def adjust_capability(capability: float, adj: float) -> float:
    """
    Adjust student capability a bit like gamma correction.
    Assumes capability is [0.0, 4.0), an assumption made elsewhere.

    :param capability: capability
    :param adj: adjustment (-1, +1) (gamma correction so negative reduces capability)
    :return: new capability
    """
    assert -10.0 < adj < +1.0

    return 4.0 * pow(capability / 4.0, 1 - adj)


def inverse_adjustment(adj: float) -> float:
    return -adj / (1.0 - adj)


def score_given_capability(capability: float, cuts: [int]) -> int:
    """
    Generate a score given a student capability. Because the capability is decimal it gives
    us what we need to interpolate between cut point levels.

    :param capability: float value [0.0, 4.0)
    :param cuts: the cut points for the levels, inc. min and max
    :return: score between min-max from cuts
    """
    level = int(math.floor(capability))
    assert 0 <= level <= len(cuts) - 2

    return int(cuts[level] + (cuts[level+1] - cuts[level]) * (capability - level))


def perf_level_given_capability(capability: float) -> int:
    """
    Return performance level given a student capability.
    Very simple method but abstracted in case capability implementation changes.

    :param capability: float value [0.0, 4.0)
    :return: 1 - 4
    """
    return int(math.floor(capability)) + 1


def random_claims(score: int, claim_weights: [float], claim_min: int, claim_max: int) -> [int]:
    """
    generate random claim scores such that

    score == sum(claim_weight[i] * claim[i] for i in NUMBER_OF_CLAIMS)
    """
    assert .999 < sum(claim_weights) < 1.001

    # shuffle the order of claims to try to even out the distribution
    # note: I don't think this actually produces a uniform distribution, but at least it doesn't treat claims
    # with the same weight differently depending on their order
    ordered = list(enumerate(claim_weights))
    random.shuffle(ordered)
    order, claim_weights = zip(*ordered)

    claims = []
    remaining_weight = 1.0

    remaining_score = score

    for claim_weight in claim_weights:
        remaining_weight -= claim_weight

        min_ = min(claim_max,
                   max(claim_min, int(math.floor((remaining_score - remaining_weight * claim_max) / claim_weight))))
        max_ = max(claim_min,
                   min(claim_max, int(math.ceil((remaining_score - remaining_weight * claim_min) / claim_weight))))

        assert min_ <= max_, "%s %s" % (min_, max_)

        claim = random.randint(min_, max_)
        claims.append(claim)

        remaining_score -= claim * claim_weight

    assert score - 1 <= sum(claims[i] * claim_weights[i] for i in range(len(claim_weights))) <= score + 1

    # unshuffle the claims
    return tuple(claims[order.index(i)] for i in range(len(claim_weights)))


def random_claim_error(claim_score: int, claim_min: int, claim_max: int):
    """Generate a std error for a claim score.
    Not sure if it is valid but this will give a larger error, the lower the score.

    :param claim_score: score
    :param claim_min: min possible score
    :param claim_max: max possible score
    :return: std error
    """
    return 40 + random.randint(0, round(80 * (claim_max - claim_score) / (claim_max - claim_min)))


def claim_perf_lvl(claim_score: int, claim_error: int, perf_cut_point: int):
    """Return claim performance level (1-3) given claim score, error and performance cut point

    :param claim_score: claim score
    :param claim_error: claim score error
    :param perf_cut_point: perf cut point, it's the third cut-point for an assessment
    :return: 1-3
    """
    if round(claim_score + 1.5 * claim_error) < perf_cut_point: return 1
    if round(claim_score - 1.5 * claim_error) >= perf_cut_point: return 3
    return 2

