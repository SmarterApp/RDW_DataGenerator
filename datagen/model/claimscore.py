"""
Model an assessment outcome claim score

"""
from datagen.model.claim import Claim


class ClaimScore:
    """
    An assessment outcome claim score
    """

    __slots__ = ('claim', 'score', 'stderr', 'perf_lvl', 'range_min', 'range_max')

    def __init__(self, claim: Claim, score: int, stderr: int, perf_lvl: int, range_min: int, range_max: int):
        self.claim = claim
        self.score = score
        self.stderr = stderr
        self.perf_lvl = perf_lvl
        self.range_min = range_min
        self.range_max = range_max
