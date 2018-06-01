"""
Model an assessment outcome claim score

"""
from data_generator.model.claim import Claim


class ClaimScore:
    """
    An assessment outcome claim score
    """

    __slots__ = ('claim', 'score', 'perf_lvl', 'range_min', 'range_max')

    def __init__(self, claim: Claim, score: int, perf_lvl: int, range_min: int, range_max: int):
        self.claim = claim
        self.score = score
        self.perf_lvl = perf_lvl
        self.range_min = range_min
        self.range_max = range_max
