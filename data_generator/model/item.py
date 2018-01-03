"""
Model an assessment item

"""


class AssessmentItem:
    """
    An assessment item
    """

    def __init__(self):
        self.bank_key = None        # e.g. '200'
        self.item_key = None        # e.g. '13958'
        self.position = None        # 1 - n
        self.segment_id = None      # should match segment id obviously
        self.type = None            # MC, EQ, MS, ...; aka format
        self.max_score = None       # 1 - n
        self.dok = None             # DoK, 1-4
        self.difficulty = None      # difficulty, -3.0 to 10
        self.operational = '1'      # '1' if operational, '0' if field test
        self.answer_key = None      # for MC,MS comma-delimited list of answers, e.g. 'A,C'
        self.options_count = 0      # for MC,MS number of answer options; e.g. 4 -> A,B,C,D
