"""
Model an item data generated for an assessment outcome (an instance of a student taking an assessment) for the assessment.

"""


class AssessmentOutcomeItemData:
    """
    An assessment outcome Item Data class.
    """

    def __init__(self):
        self.student_id = None
        self.key = None         # TODO - somehow, key+bank_key = itemId?
        self.bank_key = None    # TODO
        self.segment_id = None
        self.position = None
        self.client_id = None
        self.operational = None
        self.is_selected = None
        self.format = None          # aka item_type, e.g. MC
        self.admin_date = None
        self.number_visits = None
        self.strand = None
        self.content_level = None
        self.page_number = None
        self.page_visits = None     # responseDuration = page_time / page_visits
        self.page_time = None       #
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
        return {'assessment_outcome_item_data': self}
