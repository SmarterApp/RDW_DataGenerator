"""
An assessment score
"""


class Score:
    """
    An assessment score (overall, alt)
    """

    __slots__ = ('code', 'score', 'stderr', 'perf_lvl', 'condition_code')

    def __init__(self, code: str, score: int = None, stderr: int = None, perf_lvl: int = None,
                 /, condition_code: str = ''):
        self.code = code
        self.score = score
        self.stderr = stderr
        self.perf_lvl = perf_lvl
        self.condition_code = condition_code or ''

