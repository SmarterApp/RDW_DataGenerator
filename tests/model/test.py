"""
Unit tests for model modules.

"""
import datetime

import datagen.generators.hierarchy as hier_gen
import datagen.generators.population as pop_gen
import datagen.generators.summative_or_ica_assessment as asmt_gen
import datagen.model.itemdata as item_lvl_data
from datagen.model.studentgroup import StudentGroup
from datagen.util.id_gen import IDGen
from tests.generators.assessment_test import generate_assessment

ID_GEN = IDGen()


def test_assessment():
    # Create necessary objects
    asmt = generate_assessment('SUM', 2015, 'ELA', 3, ID_GEN)

    assert asmt.is_summative()
    assert not asmt.is_iab()


def test_assessment_outcome():
    # Create necessary objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    asmt = generate_assessment('SUM', 2015, 'ELA', 3, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(datetime.date(2015, 5, 15), student, asmt, ID_GEN)


def test_institution_hierarchy():
    # Create necessary objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    ih = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)


def test_registration_system():
    # Create necessary objects
    reg_sys = hier_gen.generate_registration_system(2015, '2014-02-25', ID_GEN)


def test_item_data():
    # Create necessary objects
    item_data = item_lvl_data.AssessmentOutcomeItemData()
    item_data.key = '1938'
    item_data.segment_id = '(SBAC)SBAC-MG110PT-S2-ELA-7-Spring-2014-2015'
    item_data.position = '19'
    item_data.format = 'MC'


def test_student():
    # Create necessary objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    reg_sys = hier_gen.generate_registration_system(2015, '2014-02-27', ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN)
    student.reg_sys = reg_sys


def test_student_set_get_groups():
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN)

    student.set_group(StudentGroup('ELA', '100', 'G3-100'))
    assert student.get_group('ELA').name == 'G3-100'
    assert student.group_1_text == 'G3-100'
    assert student.group_2_text is None

    student.set_group(StudentGroup('ELA', '200', 'G3-200'))
    student.set_group(StudentGroup('Math', '300', 'G3-300'))
    student.set_group(StudentGroup('ELPAC', '400', 'G3-400'))

    assert student.get_group('ELA').name == 'G3-200'
    assert student.get_group('Math').name == 'G3-300'
    assert student.get_group('ELPAC').name == 'G3-400'

    assert student.group_1_text == 'G3-200'
    assert student.group_2_text == 'G3-300'
    assert student.group_3_text == 'G3-400'
