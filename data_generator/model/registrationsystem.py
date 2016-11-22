"""
Model a registration system

"""


class RegistrationSystem:
    """
    A registration system.
    """

    def __init__(self):
        self.guid = None
        self.guid_sr = None
        self.sys_guid = None
        self.academic_year = None
        self.extract_date = None
        self.callback_url = None

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'registration_system': self}
