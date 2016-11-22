"""
Model the SBAC-specific items of a state.

"""

from data_generator.model.state import State


class SBACState(State):
    """
    The SBAC-specific state class.
    """

    def __init__(self):
        super().__init__()
        self.guid_sr = None
