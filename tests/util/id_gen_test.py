"""
Unit tests for the project.sbac.util.id_gen module.

"""

import re

from datagen.util.id_gen import IDGen

GUID_REGEX = '[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}'
SR_GUID_REGEX = '[a-f0-9]{30}'


def test_rec_id():
    idg = IDGen()
    id = idg.get_rec_id('some_object_type')
    assert isinstance(id, int)
    assert id == 1000000000


def test_group_id():
    idg = IDGen()
    id = idg.get_group_id('some_object_type')
    assert isinstance(id, int)
    assert id == 100


def test_rec_id_from_two_types():
    idg = IDGen()
    assert idg.get_group_id('some_object_type_1') == 100
    assert idg.get_group_id('some_object_type_2') == 100


def test_rec_id_from_two_types_bigger():
    idg = IDGen()
    assert idg.get_rec_id('some_object_type_1') == 1000000000
    assert idg.get_rec_id('some_object_type_2') == 1000000000


def test_guid():
    idg = IDGen()
    assert re.match(GUID_REGEX, idg.get_uuid())


def test_district_id():
    idg = IDGen()

    for _ in range(0, 10):
        assert re.match('^06[0-9]{5}$', idg.get_district_id('06'))


def test_school_id():
    idg = IDGen()
    assert re.match('^8880012[0-9]{7}$', idg.get_school_id('88800120000000'))
    for _ in range(0, 10):
        assert re.match('^0603465[0-9]{5}$', idg.get_school_id('0603465'))


def test_student_id():
    idg = IDGen()
    for _ in range(0, 10):
        assert re.match('^[1-9][0-9]{9}$', idg.get_student_id())
