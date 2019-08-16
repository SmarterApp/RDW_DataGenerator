"""
Model an assessment scorable (claim, alt, overall)

"""


class Scorable:
    """
    Info about something (claim, alt, overall) that is scorable
    """

    __slots__ = ('code', 'name', 'score_min', 'score_max', 'cut_points', 'weight')

    def __init__(self, code: str = None, name: str = None,
                 score_min: int = None, score_max: int = None, cut_points: [int] = None):
        self.code = code              # e.g. SOCK_R
        self.name = name              # e.g. Reading
        self.score_min = score_min    # e.g. 2250
        self.score_max = score_max    # e.g. 2780
        self.cut_points = cut_points  # list of cut_points
        self.weight = None            # e.g. 0.25

    def get_cuts(self):
        """
        Return a list of cut-points including min/max values
        :return: list of cut-points including min/max values
        """
        return [self.score_min] + (self.cut_points if self.cut_points else []) + [self.score_max]
