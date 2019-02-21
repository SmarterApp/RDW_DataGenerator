"""
Model an assessment outcome target score

"""


class TargetScore:
    """
    An assessment outcome target score
    """

    __slots__ = ('id', 'student_residual', 'standard_met_residual')

    def __init__(self, id: str, student_residual: float, standard_met_residual: float):
        self.id = id
        self.student_residual = student_residual
        self.standard_met_residual = standard_met_residual
