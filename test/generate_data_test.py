"""
Unit tests for the generate_data module.

"""

import data_generator.worker_manager as generate_data
from data_generator.util.id_gen import IDGen

ID_GEN = IDGen()


def test_set_configuration_regular():
    # Tests
    assert len(generate_data.ASMT_YEARS) == 3
    assert 2017 in generate_data.ASMT_YEARS
    assert 2018 in generate_data.ASMT_YEARS
    assert 2019 in generate_data.ASMT_YEARS
