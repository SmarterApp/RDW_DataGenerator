"""
Unit tests for the population module.

"""

import re

import datagen.config.cfg as cfg
import datagen.generators.hierarchy as hier_gen
import datagen.generators.population as pop_gen
from datagen.model.staff import TeachingStaff
from datagen.model.student import Student
from datagen.util.id_gen import IDGen

ID_GEN = IDGen()

GUID_REGEX = '[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}'


def test_generate_staff():
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    staff = pop_gen.generate_teaching_staff_member(school, ID_GEN)

    # Tests
    assert isinstance(staff, TeachingStaff)


def test_generate_student():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)

    # Tests
    assert isinstance(student, Student)
    assert re.match('[0-9]+', student.id)
    assert re.match('[a-f0-9]+', student.external_ssid)
    assert student.school_entry_date.year == 2003
    assert student.school_entry_date.month in [8, 9]


def test_advance_student_advanced():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    midl_school = hier_gen.generate_school('Middle School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(midl_school, 6, ID_GEN, 2015)
    schools_by_grade = {grade: [midl_school] for grade in midl_school.grades}

    # Test
    assert pop_gen.advance_student(student, schools_by_grade, hold_back_rate=0)


def test_advance_student_held_back():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    midl_school = hier_gen.generate_school('Middle School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(midl_school, 6, ID_GEN, 2015)
    schools_by_grade = {grade: [midl_school] for grade in midl_school.grades}

    # Test
    assert pop_gen.advance_student(student, schools_by_grade, hold_back_rate=1, drop_out_rate=0)


def test_advance_student_drop_out():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    high_school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(high_school, 11, ID_GEN, 2015)
    schools_by_grade = {grade: [high_school] for grade in high_school.grades}

    # Test
    assert not pop_gen.advance_student(student, schools_by_grade, hold_back_rate=1, drop_out_rate=1)


def test_repopulate_school_grade_empty():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    elem_school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school.config['students']['min'], elem_school.config['students']['max'] = 100, 100
    elem_school.config['students']['avg'] = 100
    students = []
    pop_gen.repopulate_school_grade(elem_school, 3, students, ID_GEN, 2015, additional_student_choice=[0])

    # Test
    assert len(students) == 100


def test_repopulate_school_grade_empty_with_additional():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    elem_school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school.config['students']['min'], elem_school.config['students']['max'] = 100, 100
    elem_school.config['students']['avg'] = 100
    students = []
    pop_gen.repopulate_school_grade(elem_school, 3, students, ID_GEN, 2015, additional_student_choice=[3])

    # Test
    assert len(students) == 103


def test_repopulate_school_grade_full_no_additional():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    elem_school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school.config['students']['min'], elem_school.config['students']['max'] = 100, 100
    elem_school.config['students']['avg'] = 100
    students = []
    for _ in range(100):
        students.append(pop_gen.generate_student(elem_school, 4, ID_GEN, 2015))
    pop_gen.repopulate_school_grade(elem_school, 4, students, ID_GEN, 2015, additional_student_choice=[0])

    # Test
    assert len(students) == 100


def test_repopulate_school_grade_full_additional():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    elem_school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school.config['students']['min'], elem_school.config['students']['max'] = 100, 100
    elem_school.config['students']['avg'] = 100
    students = []
    for _ in range(100):
        students.append(pop_gen.generate_student(elem_school, 4, ID_GEN, 2015))
    pop_gen.repopulate_school_grade(elem_school, 4, students, ID_GEN, 2015, additional_student_choice=[2])

    # Test
    assert len(students) == 102


def test_repopulate_school_grade_almost_full_additional():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    elem_school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    elem_school.config['students']['min'], elem_school.config['students']['max'] = 100, 100
    elem_school.config['students']['avg'] = 100
    students = []
    for _ in range(99):
        students.append(pop_gen.generate_student(elem_school, 4, ID_GEN, 2015))
    pop_gen.repopulate_school_grade(elem_school, 4, students, ID_GEN, 2015, additional_student_choice=[2])

    # Test
    assert len(students) == 102


def test_generate_derived_demographic_no_ethnicities():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()

    # Test
    assert pop_gen._generate_derived_demographic(student) == -1


def test_generate_derived_demographic_amer_ind():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_amer_ind = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 4


def test_generate_derived_demographic_asian():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_asian = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 2


def test_generate_derived_demographic_filipino():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_filipino = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 2


def test_generate_derived_demographic_black():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_black = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 1


def test_generate_derived_demographic_hispanic():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_hispanic = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 3


def test_generate_derived_demographic_multi():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_multi = True
    student.eth_black = True
    student.eth_pacific = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 7


def test_generate_derived_demographic_multi_hispanic():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_multi = True
    student.eth_hispanic = True
    student.eth_pacific = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 3


def test_generate_derived_demographic_none():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_none = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 0


def test_generate_derived_demographic_pacific():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_pacific = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 5


def test_generate_derived_demographic_white():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.reset_ethnicity()
    student.eth_white = True

    # Test
    assert pop_gen._generate_derived_demographic(student) == 6


def test_set_lang_items_not_lep():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.prg_lep = False
    student.lang_code = None
    student.lang_prof_level = None
    student.lang_title_3_prg = None
    student.prg_lep_entry_date = None
    student.prg_lep_exit_date = None
    pop_gen._set_lang_items(student, ifep_rate=0)

    # Tests
    assert student.lang_code is None
    assert student.lang_prof_level is None
    assert student.lang_title_3_prg is None
    assert student.prg_lep_entry_date is None
    assert student.prg_lep_exit_date is None


def test_set_lang_items_lep():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.prg_lep = True
    student.lang_code = None
    student.lang_prof_level = None
    student.lang_title_3_prg = None
    student.prg_lep_entry_date = None
    student.prg_lep_exit_date = None
    pop_gen._set_lang_items(student, lep_proficiency_levels_exit=[])

    # Tests
    assert student.lang_code in cfg.LEP_LANGUAGE_CODES
    assert student.lang_prof_level in cfg.LEP_PROFICIENCY_LEVELS
    assert student.lang_title_3_prg in cfg.LEP_TITLE_3_PROGRAMS


def test_set_lang_items_lep_no_entry_date():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.prg_lep = True
    student.lang_code = None
    student.lang_prof_level = None
    student.lang_title_3_prg = None
    student.prg_lep_entry_date = None
    student.prg_lep_exit_date = None
    pop_gen._set_lang_items(student, lep_has_entry_date_rate=0)

    # Tests
    assert student.prg_lep_entry_date is None


def test_set_lang_items_lep_entry_date_not_exited():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.prg_lep = True
    student.lang_code = None
    student.lang_prof_level = None
    student.lang_title_3_prg = None
    student.prg_lep_entry_date = None
    student.prg_lep_exit_date = None
    pop_gen._set_lang_items(student, lep_has_entry_date_rate=1, lep_proficiency_levels_exit=[])

    # Tests
    assert student.lang_title_3_prg in cfg.LEP_TITLE_3_PROGRAMS
    assert student.prg_lep_entry_date is not None
    assert student.prg_lep_exit_date is None


def test_set_lang_items_lep_entry_date_exited():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Big Average', state, ID_GEN)
    school = hier_gen.generate_school('High School', district, ID_GEN, interim_asmt_rate=1)
    student = pop_gen.generate_student(school, 11, ID_GEN, 2015)
    student.prg_lep = True
    student.lang_code = None
    student.lang_prof_level = None
    student.lang_title_3_prg = None
    student.prg_lep_entry_date = None
    student.prg_lep_exit_date = None
    pop_gen._set_lang_items(student, lep_has_entry_date_rate=1, lep_proficiency_levels=['good'],
                            lep_proficiency_levels_exit=['good'])

    # Tests
    assert student.lang_title_3_prg is None
    assert student.prg_lep_entry_date is not None
    assert student.prg_lep_exit_date is not None
