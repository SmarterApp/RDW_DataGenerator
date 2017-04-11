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
        self.operational = '1'      # '1' if operational, '0' if field test
