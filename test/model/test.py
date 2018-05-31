"""
Unit tests for model modules.

"""
import datetime

import data_generator.generators.hierarchy as hier_gen
import data_generator.generators.population as pop_gen
import data_generator.generators.summative_or_ica_assessment as asmt_gen
import data_generator.model.itemdata as item_lvl_data
from data_generator.util.id_gen import IDGen

ID_GEN = IDGen()


def test_assessment_get_object_set():
    # Create necessary objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)

    assert asmt.is_summative()
    assert not asmt.is_iab()

    # Tests
    objs = asmt.get_object_set()
    assert len(objs) == 2
    assert 'assessment' in objs
    assert objs['assessment'].guid == asmt.guid
    assert 'assessment_effective' in objs
    assert len(objs['assessment_effective']['date']) == 8


def test_assessment_outcome_get_object_set():
    # Create necessary objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(datetime.date(2015, 5, 15), student, asmt, ID_GEN)

    # Tests
    objs = asmt_out.get_object_set()
    assert len(objs) == 6
    assert 'state' in objs
    assert objs['state'].guid == state.guid
    assert 'district' in objs
    assert objs['district'].guid == district.guid
    assert 'school' in objs
    assert objs['school'].guid == school.guid
    assert 'student' in objs
    assert objs['student'].guid == student.guid
    assert 'assessment' in objs
    assert objs['assessment'].guid == asmt.guid
    assert 'assessment_outcome' in objs
    assert objs['assessment_outcome'].guid == asmt_out.guid


def test_institution_hierarchy_get_object_set():
    # Create necessary objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    ih = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)

    # Tests
    objs = ih.get_object_set()
    assert len(objs) == 4
    assert 'state' in objs
    assert objs['state'].guid == state.guid
    assert 'district' in objs
    assert objs['district'].guid == district.guid
    assert 'school' in objs
    assert objs['school'].guid == school.guid
    assert 'institution_hierarchy' in objs
    assert objs['institution_hierarchy'].guid == ih.guid


def test_registration_system_get_object_set():
    # Create necessary objects
    reg_sys = hier_gen.generate_registration_system(2015, '2014-02-25', ID_GEN)

    # Tests
    objs = reg_sys.get_object_set()
    assert len(objs) == 1
    assert 'registration_system' in objs
    assert objs['registration_system'].guid == reg_sys.guid


def test_item_data_get_object_set():
    # Create necessary objects
    item_data = item_lvl_data.AssessmentOutcomeItemData()
    item_data.key = '1938'
    item_data.segment_id = '(SBAC)SBAC-MG110PT-S2-ELA-7-Spring-2014-2015'
    item_data.position = '19'
    item_data.format = 'MC'

    # Tests
    objs = item_data.get_object_set()
    assert len(objs) == 2
    assert 'assessment_item' in objs
    assert 'assessment_outcome_item_data' in objs


def test_student_get_object_set():
    # Create necessary objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    reg_sys = hier_gen.generate_registration_system(2015, '2014-02-27', ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN)
    student.reg_sys = reg_sys

    # Tests
    objs = student.get_object_set()
    assert len(objs) == 5
    assert 'state' in objs
    assert objs['state'].guid == state.guid
    assert 'district' in objs
    assert objs['district'].guid == district.guid
    assert 'school' in objs
    assert objs['school'].guid == school.guid
    assert 'registration_system' in objs
    assert objs['registration_system'].guid == reg_sys.guid
    assert 'student' in objs
    assert objs['student'].guid == student.guid
