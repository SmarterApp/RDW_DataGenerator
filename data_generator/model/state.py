"""
Model the core of a state.

"""

from data_generator import run_id as global_run_id


class State:
    """The core of a state.
    """

    def __init__(self):
        self.run_id = global_run_id
        self.guid = None
        self.name = None
        self.code = None
        self.type_str = None
        self.config = None
        self.demo_config = None
