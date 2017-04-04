"""
Model an item data generated for an assessment outcome.

"""


class AssessmentOutcomeItemData:
    """
    An assessment outcome Item Data class.
    """

    def __init__(self):
        self.student_id = None
        self.item = None
        self.admin_date = None
        self.number_visits = None
        self.strand = None
        self.content_level = None
        self.page_number = None
        self.page_visits = None     # responseDuration = page_time / page_visits
        self.page_time = None  #
        self.dropped = None
        self.response_date = None
        self.response_value = None
        self.score = None
        self.score_status = None

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'assessment_item': self.item,
                'assessment_outcome_item_data': self}
