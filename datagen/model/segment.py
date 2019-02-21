"""
Model an assessment segment

"""


class AssessmentSegment:
    """
    An assessment segment
    """

    def __init__(self):
        self.id = None              # unique within assessment
        self.position = 1           # 1 - n
        self.algorithm = 'Fixed'
        self.algorithm_version = '0'
