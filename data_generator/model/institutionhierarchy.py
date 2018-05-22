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

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'state': self.state,
                'district': self.district,
                'school': self.school,
                'institution_hierarchy': self}
