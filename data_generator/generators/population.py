"""
Generate population elements.
"""

import calendar
import datetime
import hashlib
import random
from math import ceil

import data_generator.config.cfg as cfg
import data_generator.config.population as pop_config
import data_generator.config.hierarchy as hier_config
import data_generator.generators.names as name_gen
from data_generator.model.district import District
from data_generator.model.school import School
from data_generator.model.staff import DistrictStaff, TeachingStaff
from data_generator.model.student import Student
from data_generator.model.studentgroup import StudentGroup
from data_generator.util.assessment_stats import Properties, RandomLevelByDemographics, random_capability, \
    adjust_capability, inverse_adjustment
from data_generator.util.id_gen import IDGen
from data_generator.util.weighted_choice import weighted_choice


def generate_district_staff_member(district: District, id_gen: IDGen=IDGen, sub_class=None):
    """Generate a district-level staff member.

    :param district: The district the staff member belongs to
    :param id_gen: id generator
    :param sub_class: The sub-class of district staff to create (if requested, must be subclass of DistrictStaff)
    :return: The staff member
    """
    s = DistrictStaff() if sub_class is None else sub_class()
    s.guid = id_gen.get_uuid()
    s.gender = random.choice(['male', 'female'])
    s.first_name, s.middle_name, s.last_name = name_gen.generate_person_name(s.gender)
    s.district = district
    return s


def generate_teaching_staff_member(school: School, id_gen: IDGen=IDGen, sub_class=None):
    """Generate a teacher in a given school.

    :param school: The school the teacher teaches in
    :param id_gen: id generator
    :param sub_class: The sub-class of teaching staff to create (if requested, must be subclass of TeachingStaff)
    :returns: The staff member
    """
    s = TeachingStaff() if sub_class is None else sub_class()
    s.guid = id_gen.get_uuid()
    s.gender = random.choice(['male', 'female'])
    s.first_name, s.middle_name, s.last_name = name_gen.generate_person_name(s.gender)
    s.school = school
    return s


def generate_student(school: School, grade, id_gen: IDGen=IDGen, acad_year=datetime.datetime.now().year,
                     subjects: [str]=cfg.SUBJECTS,
                     military_connected_dist=pop_config.MILITARY_CONNECTED_DIST,
                     has_email_address_rate=pop_config.HAS_EMAIL_ADDRESS_RATE,
                     has_physical_address_rate=pop_config.HAS_PHYSICAL_ADDRESS_RATE,
                     has_address_line_2_rate=pop_config.HAS_ADDRESS_LINE_2_RATE):
    """
    Generate a student.

    :param school: The school the student belongs to
    :param grade: The grade the student belongs to
    :param id_gen: id generator
    :param acad_year: The current academic year this student is being created for (optional, defaults to your machine
                      clock's current year)
    :param subjects: list of subjects (for generating student capability)
    :param has_email_address_rate: The rate at which to generate an email address for the student
    :param has_physical_address_rate: The rate at which to generate a physical address for the student
    :param has_address_line_2_rate: The rate at which to generate a line two address for the student
    :return: The student
    """
    # Build student basics
    s = Student()
    s.guid = id_gen.get_uuid()
    s.grade = grade
    s.school = school
    s.dob = _determine_student_dob(s.grade, acad_year)

    # Determine demographics
    (gender, ethnicities, iep, sec504, lep, ed) = _determine_demographics(school.demo_config[str(grade)])
    s.gender = gender
    s.prg_iep = iep
    s.prg_sec504 = sec504
    s.prg_lep = lep
    s.prg_econ_disad = ed

    if 'amer_ind' in ethnicities:
        s.eth_amer_ind = True
    if 'black' in ethnicities:
        s.eth_black = True
    if 'hispanic' in ethnicities:
        s.eth_hispanic = True
    if 'asian' in ethnicities:
        s.eth_asian = True
    if 'filipino' in ethnicities:
        s.eth_filipino = True
    if 'pac_isl' in ethnicities:
        s.eth_pacific = True
    if 'white' in ethnicities:
        s.eth_white = True
    if 'multi' in ethnicities:
        s.eth_multi = True
    if 'none' in ethnicities:
        s.eth_none = True

    # Create the name
    s.first_name, s.middle_name, s.last_name = name_gen.generate_person_name(s.gender)

    # Create physical and email addresses
    if random.random() < has_email_address_rate:
        # Email address (first.last.#@example.com)
        s.email = s.first_name + '.' + s.last_name + '.' + str(random.randint(1, 5000)) + '@example.com'

    if random.random() < has_physical_address_rate:
        s.address_line_1 = name_gen.generate_street_address_line_1()
        if random.random() < has_address_line_2_rate:
            s.address_line_2 = name_gen.generate_street_address_line_2()
        s.address_city = name_gen.generate_street_address_city()
        s.address_zip = random.randint(10000, 99999)

    # Get the demographic config
    demo_config = school.demo_config[str(grade)]

    # Set other specifics
    s.state = school.district.state
    s.district = school.district
    s.id = id_gen.get_student_id()
    s.external_ssid = hashlib.md5(s.id.encode('utf-8')).hexdigest()
    s.rec_id = id_gen.get_rec_id('student')
    s.school_entry_date = _generate_date_enter_us_school(s.grade, acad_year)
    s.derived_demographic = _generate_derived_demographic(s)
    s.prg_migrant = determine_demo_option_selected(demo_config['migrant'])
    s.prg_idea = determine_demo_option_selected(demo_config['idea'])
    s.prg_primary_disability = random.choice(cfg.PRG_DISABILITY_TYPES)
    s.military_connected = _pick_demo_option(military_connected_dist)

    # None-out primary disability if it doesn't make sense
    if not s.prg_iep and not s.prg_idea and not s.prg_sec504:
        s.prg_primary_disability = None

    # Set language items
    _set_lang_items(s, acad_year)

    # generate and store the student's capability based on demographics and school adjustment
    adj = hier_config.SCHOOL_TYPES[school.type_str]['students'].get('adjust_pld', 0.0)
    for subject in subjects:
        # hack to make performance in ELPAC reflect student's english-learner status
        subject_adj = adj
        if subject == 'ELPAC' and s.elas == 'EL' and cfg.LEP_PROFICIENCY_LEVELS.index(s.lang_prof_level) < 3:
            subject_adj += 0.4 * (cfg.LEP_PROFICIENCY_LEVELS.index(s.lang_prof_level) - 3)
        generator, demo = _get_level_demographics(s, subject)
        s.capability[subject] = random_capability(generator.distribution(demo), subject_adj)

    return s


def advance_student(student: Student, schools_by_grade, hold_back_rate=pop_config.STUDENT_HOLD_BACK_RATE,
                    drop_out_rate=pop_config.STUDENT_DROP_OUT_RATE, transfer_rate=pop_config.STUDENT_TRANSFER_RATE):
    """Take a student and advance them to the next grade. If the next grade takes the student out of the current school,
    pick a new school for them to go to. Should that new grade not be available in any school, the student will be
    marked to drop out of the system.

    :param student: The student to move
    :param schools_by_grade: Potential new schools for a student to be enrolled in
    :param hold_back_rate: The rate at which a student should be held back from a new grade
    :param drop_out_rate: The rate that a student will drop out at if they are not advanced
    :param transfer_rate: The rate at which a student will transfer to a new school without being forced to by grade
                          boundaries
    :returns: True if the student still exists in the system, False if they do not
    """

    # clear flags
    student.held_back = False
    student.transfer = False

    # Now check if this student should be advanced
    if random.random() < hold_back_rate:
        # The student is not being advanced
        # Decide if the student should drop out and make sure the student's grade is valid
        #   If the student's grade is not valid, we could accidentally return True
        #   Return False to indicate the student is dropped out
        student.held_back = True
        if random.random() < drop_out_rate:
            # The student is being dropped out, so make them go away
            return False
        else:
            # If the student is not being advanced, but is still in a valid grade, return True
            return student.grade in schools_by_grade

    # Bump the grade
    student.grade += 1

    # If the new grade is not available in any school, drop the student
    if student.grade not in schools_by_grade:
        return False

    # changes in the student situation may change their capability
    adjustments = []

    # If the new grade of the student is not available in the school, pick a new school
    if student.grade not in student.school.grades or random.random() < transfer_rate:
        student.transfer = True
        # apply capability adjustments by undoing old school and applying new school
        adjustments.append(inverse_adjustment(hier_config.SCHOOL_TYPES[student.school.type_str]['students'].get('adjust_pld', 0.0)))
        student.school = random.choice(schools_by_grade[student.grade])
        adjustments.append(hier_config.SCHOOL_TYPES[student.school.type_str]['students'].get('adjust_pld', 0.0))

    # SmarterBalanced wants to see students get better so apply a small adjustment each time they advance
    adjustments.append(0.1)
    _apply_capability_adjustments(student, adjustments)

    return True


def determine_demo_option_selected(sub_config):
    """Decide if a boolean characteristic is selected (is true).

    :param sub_config: A dictionary for a single boolean characteristic
    :returns: If the characteristic is selected
    """
    rand_val = random.random()
    if rand_val < sub_config['perc']:
        return True
    return False


def _determine_student_dob(grade, acad_year=datetime.datetime.now().year):
    """Generates an appropriate date of birth given the student's current grade

    :param grade: The current grade of the student
    :param acad_year: The current academic year this student is being created for (optional, defaults to your machine
                      clock's current year)
    :return: A string representation of the student's date of birth
    """
    approx_age = grade + 6
    birth_year = acad_year - approx_age

    if calendar.isleap(birth_year):
        bday_offset = random.randint(0, 365)
    else:
        bday_offset = random.randint(0, 364)

    # construct a birth date as an offset from January 1st
    return datetime.date(birth_year, 1, 1) + datetime.timedelta(days=bday_offset)


def _determine_demographics(config):
    """Determine the demographic characteristics for a student based on the configuration dictionary.

    :param config: Demographics configuration dictionary to use
    :returns: A tuple of characteristics
    """
    # Determine characteristics
    gender = _pick_demo_option(config['gender'])
    ethnicity = _pick_demo_option(config['ethnicity'])
    iep = determine_demo_option_selected(config['iep'])
    sec504 = determine_demo_option_selected(config['504'])
    lep = determine_demo_option_selected(config['lep'])
    ed = determine_demo_option_selected(config['econ_dis'])

    # Pick more ethnicities if needed
    if ethnicity == 'multi':
        eth1 = 'multi'
        eth2 = 'multi'
        while eth1 == 'multi' or eth2 == 'multi':
            eth1 = _pick_demo_option(config['ethnicity']) if eth1 == 'multi' else eth1
            eth2 = _pick_demo_option(config['ethnicity']) if eth2 == 'multi' else eth2
        ethnicities = ['multi', eth1, eth2]
    else:
        ethnicities = [ethnicity]

    # Return the characteristics
    return gender, ethnicities, iep, sec504, lep, ed


def _pick_demo_option(sub_config):
    """Pick a single demographic characteristic from a dict of options.

    :param sub_config: A dictionary for a single multi-select characteristic
    :returns: Selected value for characteristic
    """
    return weighted_choice({name: obj['perc'] for name, obj in sub_config.items()})


def _get_level_demographics(student: Student, subject):
    """
    Creates the assessment stats generator and corresponding student demographics.
    They can be used to make calls in RandomLevelByDemographics like random_level and distribution

    :param student: student
    :param subject: assessment subject
    :return: RandomLevelByDemographics and student properties
    """
    # hack for custom subjects
    if subject not in cfg.LEVELS_BY_GRADE_BY_SUBJ: subject = 'Math'

    demographics = cfg.DEMOGRAPHICS_BY_GRADE[student.grade]
    level_breakdowns = cfg.LEVELS_BY_GRADE_BY_SUBJ[subject][student.grade]
    level_generator = RandomLevelByDemographics(demographics, level_breakdowns)

    student_race = ('dmg_eth_2mr' if student.eth_multi else
                    'dmg_eth_ami' if student.eth_amer_ind else
                    'dmg_eth_asn' if student.eth_asian else
                    'dmg_eth_asn' if student.eth_filipino else   # yes, treating filipino as asian for perf
                    'dmg_eth_blk' if student.eth_black else
                    'dmg_eth_hsp' if student.eth_hispanic else
                    'dmg_eth_pcf' if student.eth_pacific else
                    'dmg_eth_wht' if student.eth_white else
                    'dmg_eth_nst')

    student_demographics = Properties(dmg_prg_504=student.prg_sec504,
                                      dmg_prg_tt1=student.prg_econ_disad,
                                      dmg_prg_iep=student.prg_iep,
                                      dmg_prg_lep=student.prg_lep,
                                      gender=student.gender,
                                      race=student_race)

    return level_generator, student_demographics


def repopulate_school_grade(school: School, grade, grade_students, id_gen, reg_sys,
                            acad_year=datetime.datetime.now().year,
                            subjects: [str]=cfg.SUBJECTS,
                            additional_student_choice=pop_config.REPOPULATE_ADDITIONAL_STUDENTS):
    """
    Take a school grade and make sure it has enough students. The list of students is updated in-place.

    @param school: The school to potentially re-populate, should have district/state set
    @param grade: The grade in the school to potentially re-populate
    @param grade_students: The students currently in the grade for this school
    @param id_gen: ID generator
    @param reg_sys: The registration system this student falls under
    @param acad_year: The current academic year that the repopulation is occurring within (optional, defaults to your
                      machine clock's current year)
    @param subjects: List of subjects (for generating new student capabilities); defaults to cfg.SUBJECTS
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
        s = generate_student(school, grade, id_gen, acad_year, subjects)
        s.reg_sys = reg_sys
        grade_students.append(s)


def assign_student_groups(school, grade, grade_students, id_gen: IDGen=IDGen, subjects: [str]=cfg.SUBJECTS):
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
    num_groups = int(ceil(len(grade_students) / school.group_size))
    for subject in subjects:
        # generate lists of subgroups for each subject corresponding to school's group size
        subgroups = []
        for _ in range(num_groups):
            group_id = id_gen.get_group_id('group')
            group_name = 'G' + str(grade) + '-' + str(group_id)
            subgroups.append((group_id, group_name))
        # assign each student a (randomly selected) group for this subject
        for grade_student in grade_students:
            (group_id, group_name) = random.choice(subgroups)
            grade_student.set_group(StudentGroup(subject, group_id, group_name))


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
        if student.eth_hispanic is True:
            return 3

        else:
            demos = {0: student.eth_none,
                     1: student.eth_black,
                     2: student.eth_asian or student.eth_filipino,
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
                    lep_has_entry_date_rate=cfg.LEP_HAS_ENTRY_DATE_RATE,
                    lep_language_codes=cfg.LEP_LANGUAGE_CODES,
                    lep_proficiency_levels=cfg.LEP_PROFICIENCY_LEVELS,
                    lep_proficiency_levels_exit=cfg.LEP_PROFICIENCY_LEVELS_EXIT,
                    lep_title_3_programs=cfg.LEP_TITLE_3_PROGRAMS,
                    ifep_rate=pop_config.IFEP_RATE):
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
    @param ifep_rate: IFEP rate
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
            student.elas = 'RFEP'
            student.elas_start_date = student.prg_lep_exit_date
        else:
            student.elas = 'EL'
            student.elas_start_date = student.prg_lep_entry_date
    else:
        # rarely set lang_code to not english, proficiency "very good", and ELAS to "IFEP"
        # IFEP = student tested out of, and never entered LEP/ELAS
        if random.random() < ifep_rate:
            student.lang_code = random.choice(lep_language_codes)
            student.lang_prof_level = random.choice(lep_proficiency_levels_exit)
            student.elas = 'IFEP'
        else:
            student.elas = 'EO'


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


def _apply_capability_adjustments(student: Student, adjustments: [float]):
    for subject, capability in student.capability.items():
        value = capability
        for adj in adjustments:
            value = adjust_capability(value, adj)
        student.capability[subject] = value
