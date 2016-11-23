"""
Unit tests for the generate_data module.

"""

import data_generator.worker_manager as generate_data
from data_generator.util.id_gen import IDGen

ID_GEN = IDGen()


def test_set_configuration_regular():
    # Tests
    assert len(generate_data.YEARS) == 3
    assert 2015 in generate_data.YEARS
    assert 2016 in generate_data.YEARS
    assert 2017 in generate_data.YEARS
    assert len(generate_data.ASMT_YEARS) == 3
    assert 2015 in generate_data.ASMT_YEARS
    assert 2016 in generate_data.ASMT_YEARS
    assert 2017 in generate_data.ASMT_YEARS
    assert len(generate_data.INTERIM_ASMT_PERIODS) == 3
    assert 'Fall' in generate_data.INTERIM_ASMT_PERIODS
    assert 'Winter' in generate_data.INTERIM_ASMT_PERIODS
    assert 'Spring' in generate_data.INTERIM_ASMT_PERIODS
