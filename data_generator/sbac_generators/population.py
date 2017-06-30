"""
Augment the generation of population elements with SBAC-specific items.

"""

import datetime
import random

from math import ceil

import data_generator.config.cfg as sbac_in_config
import data_generator.generators.population as general_pop_gen
from data_generator.config import cfg
from data_generator.model.school import School
from data_generator.model.staff import TeachingStaff
from data_generator.model.student import Student
from data_generator.util.id_gen import IDGen


def generate_student(school: School, grade, id_gen, state, acad_year=datetime.datetime.now().year):
    """
    Generate a student.

    @param school: The school the student belongs to
    @param grade: The grade the student belongs to
    @param id_gen: ID generator
    @param state: The state this student falls within
    @param acad_year: The current academic year this student is being created for (optional, defaults to your machine
                      clock's current year)
    @return: The student
    """
    # Run the General generator
    s = general_pop_gen.generate_student(school, grade, acad_year, Student)

    # Get the demographic config
    demo_config = school.demo_config[str(grade)]

    # Set other specifics
    s.state = state
    s.district = school.district
    s.rec_id = id_gen.get_rec_id('student')
    s.rec_id_sr = id_gen.get_rec_id('sr_student')
    s.guid_sr = id_gen.get_sr_uuid()
    s.external_ssid = s.guid + 'ext'
    s.external_ssid_sr = id_gen.get_sr_uuid()
    s.school_entry_date = _generate_date_enter_us_school(s.grade, acad_year)
    s.derived_demographic = _generate_derived_demographic(s)
    s.prg_migrant = general_pop_gen.determine_demo_option_selected(demo_config['migrant'])
    s.prg_idea = general_pop_gen.determine_demo_option_selected(demo_config['idea'])
    s.prg_primary_disability = random.choice(sbac_in_config.PRG_DISABILITY_TYPES)
    s.skip_iab = random.random() < sbac_in_config.IAB_STUDENT_RATE

    # None-out primary disability if it doesn't make sense
    if not s.prg_iep and not s.prg_idea and not s.prg_sec504:
        s.prg_primary_disability = None

    # Set language items
    _set_lang_items(s, acad_year)

    return s


def advance_student(student: Student, schools_by_grade, hold_back_rate=sbac_in_config.HOLD_BACK_RATE,
                    drop_out_rate=sbac_in_config.NOT_ADVANCED_DROP_OUT_RATE,
                    transfer_rate=sbac_in_config.TRANSFER_RATE):
    """
    Take a student and advance them to the next grade. If the next grade takes the student out of the current school,
    pick a new school for them to go to.

    @param student: The student to move
    @param schools_by_grade: Potential new schools for a student to be enrolled in
    @param drop_out_rate: The rate (chance) that a student will drop out at if they are not advanced
    @returns: True if the student still exists in the system, False if they do not
    """
    # Use the general generator to advance the student
    rslt = general_pop_gen.advance_student(student, schools_by_grade, hold_back_rate=hold_back_rate,
                                           drop_out_rate=drop_out_rate, transfer_rate=transfer_rate)

    # If we are not keeping the student, don't worry about them
    if not rslt:
        return rslt

    # TODO: Change things like LEP status or IEP status, etc

    return True


def repopulate_school_grade(school: School, grade, grade_students, id_gen, state, reg_sys,
                            acad_year=datetime.datetime.now().year,
                            additional_student_choice=sbac_in_config.REPOPULATE_ADDITIONAL_STUDENTS):
    """
    Take a school grade and make sure it has enough students. The list of students is updated in-place.

    @param school: The school to potentially re-populate
    @param grade: The grade in the school to potentially re-populate
    @param grade_students: The students currently in the grade for this school
    @param id_gen: ID generator
    @param state: The state these potential new students will fall within
    @param reg_sys: The registration system this student falls under
    @param acad_year: The current academic year that the repopulation is occurring within (optional, defaults to your
                      machine clock's current year)
    @param additional_student_choice: Array of values for additional students to create in the grade
    """
    # Calculate a new theoretically student count
    if school.student_count_min < school.student_count_max:
        student_count = int(random.triangular(school.student_count_min, school.student_count_max,
                                              school.student_count_avg))
    else:
        student_count = school.student_count_min

    # Add in additional students
    student_count = student_count + random.choice(additional_student_choice)

    # Re-fill grade to this new student count
    while len(grade_students) < student_count:
        s = generate_student(school, grade, id_gen, state, acad_year)
        s.reg_sys = reg_sys
        grade_students.append(s)


def assign_student_groups(school, grade, grade_students, id_gen=IDGen(), subjects=cfg.SUBJECTS):
    """
    Assign students to groups.
    Each student is assigned to one group per subject. The groups assigned correspond
    to the subjects, so group_1 -> subjects[0], group_2 -> subjects[1], etc. The student
    group is overwritten if there is already one set.
    Currently, there are no "staff_based" groups assigned.
    
    @param school: The school
    @param grade: The grade in the school to assign groupings to.
    @param grade_students: The students currently in the grade for this school
    @param id_gen: The IDGen instance, used to make groups unique across multiple schools
    @param subjects: The list of subjects
    """
    # generate lists of subgroups for each subject corresponding to school's group size
    num_groups = int(ceil(len(grade_students) / school.group_size))
    groups = []
    for _ in subjects:
        subgroups = []
        for _ in range(num_groups):
            group_id = id_gen.get_group_id('group')
            group_name = 'G' + str(grade) + '-' + str(group_id)
            subgroups.append((group_id, group_name))
        groups.append(subgroups)

    for (i, subgroups) in enumerate(groups, start=1):
        for grade_student in grade_students:
            (group_id, group_name) = random.choice(subgroups)
            setattr(grade_student, "group_%i_id" % (i,), group_id)
            setattr(grade_student, "group_%i_text" % (i,), group_name)


def generate_teaching_staff_member(school: School, id_gen):
    """
    Generate a teaching_staff for the given school.

    @param school: School for which staff to generate
    @param id_gen: ID generator
    @returns: The staff_member
    """
    # Run the general generator
    s = general_pop_gen.generate_teaching_staff_member(school, TeachingStaff)

    # Set the SR guid
    s.guid_sr = id_gen.get_sr_uuid()

    return s


def _generate_date_enter_us_school(grade, acad_year=datetime.datetime.now().year):
    """
    Generates an appropriate date of when a student would have entered a US school, assuming all students entered
    school in grade K.

    @param grade: the current grade of the student
    @param acad_year: The current academic year to use to create the date (optional, defaults to your machine clock's
                      current year)
    @return: a date object that represents the student's entry date
    """
    entry_year = acad_year - grade - 1
    entry_month = random.randint(8, 9)
    entry_day = random.randint(15, 31) if entry_month == 8 else random.randint(1, 15)
    return datetime.date(entry_year, entry_month, entry_day)


def _generate_derived_demographic(student):
    """
    Generate the derived demographic value for a student.

    @param student: Student to calculate value for
    @returns: Derived demographic value
    """
    try:
        # TODO: need to decide the value. is it true/false, or f/t, or others
        if student.eth_hispanic is True:
            return 3

        else:
            demos = {0: student.eth_none,
                     1: student.eth_black,
                     2: student.eth_asian,
                     4: student.eth_amer_ind,
                     5: student.eth_pacific,
                     6: student.eth_white}

            races = [demo for demo, value in demos.items() if value]

            if len(races) > 1:
                return 7  # multi-racial
            elif len(races) == 1:
                return races[0]
            else:
                raise Exception('No race?')
    except Exception as ex:
        print('Generate derived demographic column error: %s' % str(ex))
        return -1


def _set_lang_items(student, acad_year=datetime.datetime.now().year,
                    lep_has_entry_date_rate=sbac_in_config.LEP_HAS_ENTRY_DATE_RATE,
                    lep_language_codes=sbac_in_config.LEP_LANGUAGE_CODES,
                    lep_proficiency_levels=sbac_in_config.LEP_PROFICIENCY_LEVELS,
                    lep_proficiency_levels_exit=sbac_in_config.LEP_PROFICIENCY_LEVELS_EXIT,
                    lep_title_3_programs=sbac_in_config.LEP_TITLE_3_PROGRAMS):
    """
    Set the language values for a student.

    @param student: The student to configure
    @param acad_year: The current academic year to use to create the date (optional, defaults to your machine clock's
                      current year)
    @param lep_has_entry_date_rate: The rate (chance) that the student has an entry date for LEP services
    @param lep_language_codes: Language codes to pick from to assign to an LEP student
    @param lep_proficiency_levels: Proficiency levels that can be assigned to an LEP student
    @param lep_proficiency_levels_exit: Proficiency levels that are good enough for the student to have exited LEP
    @param lep_title_3_programs: Title 3 programs that can be assigned to an LEP student
    """
    if student.prg_lep:
        # Pick a random non-English language
        student.lang_code = random.choice(lep_language_codes)
        student.lang_prof_level = random.choice(lep_proficiency_levels)
        student.lang_title_3_prg = random.choice(lep_title_3_programs)

        # Decide if to set entry date for LEP
        if random.random() < lep_has_entry_date_rate:
            student.prg_lep_entry_date = _generate_date_lep_entry(student.grade, acad_year)

        # Set an exit date if the proficiency level is good enough
        if student.lang_prof_level in lep_proficiency_levels_exit:
            student.prg_lep_exit_date = _generate_date_lep_exit(student.grade, acad_year)
            student.lang_title_3_prg = None


def _generate_date_lep_entry(grade, acad_year=datetime.datetime.now().year):
    """
    Generates an appropriate date of when a student would have been designated as LEP

    @param grade: the current grade of the student
    @return: a date object that represents the student's entry date
    """
    entry_year = acad_year - (grade if grade < 5 else random.randint(4, grade))
    entry_month = random.randint(8, 9)
    entry_day = random.randint(15, 31) if entry_month == 8 else random.randint(1, 15)
    return datetime.date(entry_year, entry_month, entry_day)


def _generate_date_lep_exit(grade, acad_year=datetime.datetime.now().year):
    """
    Generates an appropriate date of when a student would have been promoted from LEP status

    @param grade: the current grade of the student
    @param acad_year: The current academic year to use to create the date (optional, defaults to your machine clock's
                      current year)
    @return: a date object that represents the student's exit date
    """
    entry_year = acad_year - (3 if grade > 3 else 1)
    entry_month = random.randint(3, 6)
    entry_day = random.randint(1, 30)
    return datetime.date(entry_year, entry_month, entry_day)
