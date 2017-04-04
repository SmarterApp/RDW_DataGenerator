"""
Unit tests for the sbac_data_generation.generators.hierarchy module.

"""

import datetime

import data_generator.sbac_generators.hierarchy as hier_gen
from data_generator.model.district import District
from data_generator.model.group import Group
from data_generator.model.school import School
from data_generator.model.state import State
from data_generator.util.id_gen import IDGen
from nose.tools import assert_is_instance, assert_raises, assert_regexp_matches

ID_GEN = IDGen()

GUID_REGEX = '[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}'
SR_GUID_REGEX = '[a-f0-9]{30}'


def test_generate_state():
    # Create object
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)

    # Tests
    assert_is_instance(state, State)
    assert state.name == 'Example State'
    assert state.code == 'ES'
    assert_regexp_matches(state.guid_sr, SR_GUID_REGEX)


def test_generate_state_invalid_type():
    assert_raises(LookupError, hier_gen.generate_state, 'unknown', 'Example State', 'ES', ID_GEN)


def test_generate_district():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)

    # Tests
    assert_is_instance(district, District)
    assert district.state == state
    assert_regexp_matches(district.guid_sr, SR_GUID_REGEX)


def test_generate_district_invalid_type():
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    assert_raises(LookupError, hier_gen.generate_district, 'unknown', state, ID_GEN)


def test_generate_school():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN)

    # Tests
    assert_is_instance(school, School)
    assert school.district == district
    assert_regexp_matches(school.guid_sr, SR_GUID_REGEX)


def test_generate_school_invalid_type():
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    assert_raises(LookupError, hier_gen.generate_school, 'unknown', district, ID_GEN)


def test_generate_group():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN)
    group = hier_gen.generate_group('section_based', school, ID_GEN)

    # Tests
    assert_is_instance(group, Group)
    assert group.school == school
    assert_regexp_matches(group.guid_sr, SR_GUID_REGEX)
    assert group.type == 'section_based'


def test_generate_group_invalid_type():
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN)
    assert_raises(LookupError, hier_gen.generate_group, 'unknown', school, ID_GEN)


def test_generate_school_no_interims():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=0)

    # Test
    assert not school.takes_interim_asmts


def test_generate_school_interims():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)

    # Test
    assert school.takes_interim_asmts


def test_generate_registration_system():
    rs = hier_gen.generate_registration_system(2015, '2014-02-15', ID_GEN)
    assert_regexp_matches(rs.guid, GUID_REGEX)
    assert_regexp_matches(rs.sys_guid, GUID_REGEX)
    assert rs.academic_year == 2015
    assert rs.extract_date == '2014-02-15'
    assert rs.callback_url == 'SateTestReg.gov/StuReg/CallBack'


def test_generate_institution_hierarchy():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN)
    ih = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)

    # Tests
    assert_is_instance(ih.rec_id, int)
    assert_regexp_matches(ih.guid, GUID_REGEX)
    assert ih.state == state
    assert ih.district == district
    assert ih.school == school
    assert ih.from_date == datetime.date(2014, 9, 1)
    assert ih.to_date == datetime.date(9999, 12, 31)


def test_sort_schools_by_grade():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    elem_school_1 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school_2 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school_3 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    midl_school_1 = hier_gen.generate_school('Middle School', district, ID_GEN)
    midl_school_2 = hier_gen.generate_school('Middle School', district, ID_GEN)
    high_school = hier_gen.generate_school('High School', district, ID_GEN)
    schools_by_grade = hier_gen.sort_schools_by_grade([elem_school_1, elem_school_2, elem_school_3, midl_school_1,
                                                       midl_school_2, high_school])

    # Tests
    assert len(schools_by_grade.keys()) == 7
    assert len(schools_by_grade[3]) == 3
    assert len(schools_by_grade[4]) == 3
    assert len(schools_by_grade[5]) == 3
    assert len(schools_by_grade[6]) == 2
    assert len(schools_by_grade[7]) == 2
    assert len(schools_by_grade[8]) == 2
    assert len(schools_by_grade[11]) == 1


def test_set_up_schools_with_grades():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    elem_school_1 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school_2 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school_3 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    midl_school_1 = hier_gen.generate_school('Middle School', district, ID_GEN)
    midl_school_2 = hier_gen.generate_school('Middle School', district, ID_GEN)
    high_school = hier_gen.generate_school('High School', district, ID_GEN)
    schools_with_grades = hier_gen.set_up_schools_with_grades([elem_school_1, elem_school_2, elem_school_3,
                                                               midl_school_1, midl_school_2, high_school],
                                                              {3, 4, 5, 6, 7, 8, 11})

    # Tests
    assert len(schools_with_grades) == 6
    assert len(schools_with_grades[elem_school_1]) == 3
    assert len(schools_with_grades[elem_school_2]) == 3
    assert len(schools_with_grades[elem_school_3]) == 3
    assert len(schools_with_grades[midl_school_1]) == 3
    assert len(schools_with_grades[midl_school_2]) == 3
    assert len(schools_with_grades[high_school]) == 1


def test_set_up_schools_with_groupings():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    elem_school_1 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school_2 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    midl_school_1 = hier_gen.generate_school('Middle School', district, ID_GEN)
    midl_school_2 = hier_gen.generate_school('Middle School', district, ID_GEN)
    high_school = hier_gen.generate_school('High School', district, ID_GEN)
    schools_with_groupings = hier_gen.set_up_schools_with_groupings([elem_school_1, elem_school_2,
                                                                     midl_school_1, midl_school_2, high_school],
                                                                    {3, 4, 5, 6, 7, 8, 11})
    # Tests
    assert len(schools_with_groupings) == 5
    assert len(schools_with_groupings[elem_school_1]) == 3
    assert len(schools_with_groupings[elem_school_2]) == 3
    assert len(schools_with_groupings[midl_school_1]) == 3
    assert len(schools_with_groupings[midl_school_2]) == 3
    assert len(schools_with_groupings[high_school]) == 1


def test_populate_schools_with_groupings():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    elem_school_1 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school_2 = hier_gen.generate_school('Elementary School', district, ID_GEN)
    midl_school_1 = hier_gen.generate_school('Middle School', district, ID_GEN)
    high_school = hier_gen.generate_school('High School', district, ID_GEN)
    schools_with_groupings = hier_gen.set_up_schools_with_groupings([elem_school_1, elem_school_2,
                                                                     midl_school_1, high_school],
                                                                    {3, 4, 5, 6, 7, 8, 11})
    pop_school_with_groupings = hier_gen.populate_schools_with_groupings(schools_with_groupings, ID_GEN)
    # Tests
    assert len(schools_with_groupings) == 4
    assert len(schools_with_groupings[elem_school_1]) == 3
    assert len(schools_with_groupings[elem_school_2]) == 3
    assert len(schools_with_groupings[midl_school_1]) == 3
    assert len(schools_with_groupings[high_school]) == 1
