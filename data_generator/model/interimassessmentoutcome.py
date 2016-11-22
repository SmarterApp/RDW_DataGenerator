"""
Model an IAB  outcome
"""

from data_generator.model.assessmentoutcome import AssessmentOutcome


class InterimAssessmentOutcome(AssessmentOutcome):
    """
    An IAB outcome class.
    """

    def __setattr__(self, name, value):
        """
        Prevent setting some values to prevent bugs due to typos etc.
        :param name:
        :param value:
        :return:
        """
        if name in {'overall_score', 'overall_score_range_min', 'overall_score_range_max', 'overall_perf_lvl',
                    'claim_2_score', 'claim_2_score_range_min', 'claim_2_score_range_max', 'claim_2_perf_lvl',
                    'claim_3_score', 'claim_3_score_range_min', 'claim_3_score_range_max', 'claim_3_perf_lvl',
                    'claim_4_score', 'claim_4_score_range_min', 'claim_4_score_range_max', 'claim_4_perf_lvl'}:
            raise AttributeError('cannot set %s of %s' % (name, self.__class__.__qualname__))

        else:
            super().__setattr__(name, value)
