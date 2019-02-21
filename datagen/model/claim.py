"""
Model an assessment (scorable) claim

"""


class Claim:
    """
    An assessment (scorable) claim
    """

    __slots__ = ('code', 'name', 'score_min', 'score_max')

    def __init__(self, code: str, name: str, score_min: int, score_max: int):
        self.code = code            # e.g. SOCK_R
        self.name = name            # e.g. Reading
        self.score_min = score_min  # e.g. 2250
        self.score_max = score_max  # e.g. 2780
