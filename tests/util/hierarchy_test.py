
import pytest

from inspect import getsourcefile
from os.path import abspath, dirname, join

from datagen.util.hierarchy import read_hierarchy, write_hierarchy

# technique for getting current directory regardless of how it is being run
test_data_dir = abspath(join(dirname(abspath(getsourcefile(lambda: 0))), '../../test_data/'))


def test_reading_hierarchy():
    state, districts, schools = read_hierarchy(join(test_data_dir, 'hierarchy.good.csv'))
    assert state is not None
    assert len(districts) == 2
    assert len(schools) == 9


def test_writing_hierarchy():
    state, districts, schools = read_hierarchy(join(test_data_dir, 'hierarchy.good.csv'))
    write_hierarchy(join(test_data_dir, 'hierarchy.good.copy.csv'), schools)


def test_value_errors():
    with pytest.raises(ValueError):
        read_hierarchy(join(test_data_dir, 'hierarchy.bad_headers.csv'))
    with pytest.raises(ValueError):
        read_hierarchy(join(test_data_dir, 'hierarchy.bad_state_type.csv'))
    with pytest.raises(ValueError):
        read_hierarchy(join(test_data_dir, 'hierarchy.bad_district_type.csv'))
    with pytest.raises(ValueError):
        read_hierarchy(join(test_data_dir, 'hierarchy.bad_school_type.csv'))
    with pytest.raises(ValueError):
        read_hierarchy(join(test_data_dir, 'hierarchy.multiple_states.csv'))
