"""
Model the core of a class.

"""

from data_generator import run_id as global_run_id


class Class:
    """The core of a class.
    """

    def __init__(self):
        self.run_id = global_run_id
        self.guid = None
        self.school = None
        self.name = None
        self.subject = None
