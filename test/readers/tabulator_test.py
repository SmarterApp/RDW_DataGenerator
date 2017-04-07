"""
Unit tests for tabulator reader methods

"""
from inspect import getsourcefile
from os.path import abspath, dirname, join

from data_generator.readers.tabulator_reader import load_assessments_file

# technique for getting current directory regardless of how it is being run
test_data_dir = abspath(join(dirname(abspath(getsourcefile(lambda:0))), '../../test_data/'))


def test_reading_english_iab_with_items():
    asmts = load_assessments_file(join(test_data_dir, 'IAB_English.items.csv'), False, False, True, True)
    assert len(asmts) == 9
    assert list(map(lambda asmt: len(asmt.item_bank), asmts)) == [6, 15, 15, 15, 4, 16, 15, 18, 15]


def test_reading_english_iab_without_items():
    asmts = load_assessments_file(join(test_data_dir, 'IAB_English.items.csv'), False, False, True, False)
    assert len(asmts) == 9
    assert asmts[0].item_bank is None


def test_reading_math_iab_with_items():
    asmts = load_assessments_file(join(test_data_dir, 'IAB_Math.items.csv'), False, False, True, True)
    assert len(asmts) == 5
    assert list(map(lambda asmt: len(asmt.item_bank), asmts)) == [15, 14, 14, 15, 6]


def test_reading_math_iab_without_items():
    asmts = load_assessments_file(join(test_data_dir, 'IAB_Math.items.csv'), False, False, True, False)
    assert len(asmts) == 5
    assert asmts[0].item_bank is None
