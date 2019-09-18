"""
An institution hierarchy

"""


class InstitutionHierarchy:
    """
    An institution hierarchy.
    """

    def __init__(self):
        self.guid = None
        self.rec_id = None      # record id, used to link output records
        self.state = None
        self.district = None
        self.school = None
        self.from_date = None
        self.to_date = None
