"""
Model a subject trait
"""


class Trait:
    """ Info about a trait
    """

    __slots__ = ('code', 'purpose', 'category', 'max_score')

    def __init__(self, code: str = None, purpose: str = None, category: str = None, max_score: int = None):
        self.code = code            # e.g. SOCK_EXPL_ORG
        self.purpose = purpose      # e.g. EXPL
        self.category = category    # e.g. ORG
        self.max_score = max_score  # e.g. 3
