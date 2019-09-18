"""
An assessment score
"""


class Score:
    """
    An assessment score (overall, alt)
    """

    __slots__ = ('code', 'score', 'stderr', 'perf_lvl')

    def __init__(self, code: str, score: int = None, stderr: int = None, perf_lvl: int = None):
        self.code = code
        self.score = score
        self.stderr = stderr
        self.perf_lvl = perf_lvl
