"""
Unit tests for tabulator reader methods

"""
from inspect import getsourcefile
from os.path import abspath, dirname, join

from datagen.readers.subject_reader import load_subject_file

# technique for getting current directory regardless of how it is being run
test_data_dir = abspath(join(dirname(abspath(getsourcefile(lambda: 0))), '../../test_data/'))


def test_reading_ELPAC():
    subject = load_subject_file(join(test_data_dir, 'ELPAC_subject.xml'))
    assert subject.code == 'ELPAC'
    assert len(subject.alts) == 2
    assert len(subject.claims) == 4
    assert len(subject.types) == 1
    sum = subject.types['SUM']
    assert sum.overall_scoring.perf_levels == 4
    assert sum.alt_scoring.perf_levels == 4
    assert sum.claim_scoring.perf_levels == 3


if __name__ == '__main__':
    test_reading_ELPAC()
