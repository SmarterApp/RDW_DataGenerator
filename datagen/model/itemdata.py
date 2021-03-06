"""
Model an item data generated for an assessment outcome.

"""


class AssessmentOutcomeItemData:
    """
    An assessment outcome Item Data class.
    """

    def __init__(self):
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
        self.is_selected = '1'      # did student attempt an answer
        self.score = None
        self.score_status = None
        self.sub_scores = None      # array of subscores: "Organization/Purpose", "Evidence/Elaboration", "Conventions"
