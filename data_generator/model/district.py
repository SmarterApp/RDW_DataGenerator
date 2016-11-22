"""
Model the core of a district.
"""

from data_generator import run_id as global_run_id


class District:
    """The core of a district.
    """

    def __init__(self):
        self.run_id = global_run_id
        self.guid = None
        self.name = None
        self.state = None
        self.type_str = None
        self.config = None
        self.demo_config = None
