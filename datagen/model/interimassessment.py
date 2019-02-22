"""
Model an IAB

"""

from datagen.model.assessment import Assessment


class InterimAssessment(Assessment):
    """
    An IAB class
    """

    def __init__(self):
        super().__init__()

    def __setattr__(self, name, value):
        """
        Prevent setting some values to prevent bugs due to typos etc.
        :param name:
        :param value:
        :return:
        """
        if name in {'overall_score_min', 'overall_score_max',
                    'overall_cut_point_1', 'overall_cut_point_2', 'overall_cut_point_3',
                    'perf_lvl_name_1', 'perf_lvl_name_2', 'perf_lvl_name_3', 'perf_lvl_name_4',
                    'claim_2_name', 'claim_2_score_min', 'claim_2_score_max',
                    'claim_3_name', 'claim_3_score_min', 'claim_3_score_max',
                    'claim_4_name', 'claim_4_score_min', 'claim_4_score_max'}:
            raise AttributeError('cannot set {} of {}'.format(name, self.__class__.__qualname__))

        else:
            super().__setattr__(name, value)
