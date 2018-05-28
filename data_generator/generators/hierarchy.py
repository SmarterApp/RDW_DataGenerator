"""Generate hierarchy components.
"""
import random

import data_generator.config.hierarchy as hier_config
import data_generator.config.population as pop_config
import data_generator.config.state_types as state_config
import data_generator.generators.names as name_gen
from data_generator.config import cfg
from data_generator.model.district import District
from data_generator.model.institutionhierarchy import InstitutionHierarchy
from data_generator.model.registrationsystem import RegistrationSystem
from data_generator.model.school import School
from data_generator.model.state import State
from data_generator.util.id_gen import IDGen


def generate_state(state_type, name, code, id_gen=IDGen, state_types=state_config.STATE_TYPES, pop_demos=pop_config.DEMOGRAPHICS):
    """Generate a state of the given state type.

    :param state_type: The type of state to generate
    :param name: The name of the state
    :param code: The two-character code of the state
    :param id_gen: id generator
    :param state_types: The state types configuration object
    :param pop_demos: The population demographics configuration object
    :returns: The state
    """
    # Validate state type
    if state_type not in state_types:
        raise LookupError("State type '" + str(state_type) + "' was not found")

    # Create the state
    s = State()
    s.guid = id_gen.get_uuid()
    s.name = name
    s.code = code
    s.type_str = state_type
    s.config = state_types[state_type]
    s.id = s.config['id'] if 'id' in s.config else '00'

    # Validate the demographics type
    if s.config['demographics'] not in pop_config.DEMOGRAPHICS:
        raise LookupError("Demographics type '" + str(s.config['demographics']) + "' was not found")

    # Store the demographics
    s.demo_config = pop_demos[s.config['demographics']]

    return s


def generate_district(district_type, state: State, id_gen=IDGen, district_types=hier_config.DISTRICT_TYPES):
    """Generate a district specified by the parameters.

    :param district_type: The type of district to generate
    :param state: The state the district belongs to
    :param district_types: The district types configuration object
    :returns: The district
    """
    # Validate district type
    if district_type not in district_types:
        raise LookupError("District type '" + str(district_type) + "' was not found")

    # Create and store the district
    d = District()
    d.guid = id_gen.get_uuid()
    d.name = name_gen.generate_district_name()
    d.state = state
    d.type_str = district_type
    d.config = district_types[district_type]
    d.demo_config = state.demo_config
    d.id = id_gen.get_district_id(state.id)

    # override external id and name (if available)
    # TODO - this isn't multithread safe
    if d.id in cfg.HIERARCHY_MAP:
        d.id, d.name = cfg.HIERARCHY_MAP[d.guid]
    elif len(cfg.EXTERNAL_DISTRICTS) > 0:
        # TODO - any way to pick district based on how many schools it will have?
        ext_district = cfg.EXTERNAL_DISTRICTS.popitem()[1]
        d.id, d.name = cfg.HIERARCHY_MAP[d.id] = (ext_district['entityId'], ext_district['entityName'])

    return d


def generate_school(school_type, district: District, id_gen=IDGen, school_types=hier_config.SCHOOL_TYPES, interim_asmt_rate=cfg.INTERIM_ASMT_RATE):
    """Generate a school specified by the parameters.

    :param school_type: The type of school to generate
    :param district: The district the school belongs to
    :param id_gen: ID generator
    :param school_types: The school types configuration object
    :param interim_asmt_rate: The rate (chance) that students in this school will take interim assessments
    :returns: The school
    """
    # Validate the school type
    if school_type not in school_types:
        raise LookupError("School type '" + str(school_type) + "' was not found")

    # Create and store the school
    s = School()
    s.guid = id_gen.get_uuid()
    s.name = name_gen.generate_school_name(hier_config.SCHOOL_TYPES[school_type]['type'])
    s.district = district
    s.type_str = school_type
    s.config = school_types[school_type]
    s.demo_config = district.demo_config
    s.id = id_gen.get_school_id(district.id)

    # override external id and name (if available)
    if s.id in cfg.HIERARCHY_MAP:
        s.id, s.name = cfg.HIERARCHY_MAP[s.guid]
    elif len(cfg.EXTERNAL_SCHOOLS) > 0:
        # find an external school that points to the correct district, if any
        for key, ext_school in cfg.EXTERNAL_SCHOOLS.items():
            if ext_school['parentEntityId'] == district.id:
                cfg.EXTERNAL_SCHOOLS.pop(key)
                s.id, s.name = cfg.HIERARCHY_MAP[s.guid] = (ext_school['entityId'], ext_school['entityName'])
                break

    # Decide if the school takes interim assessments
    if random.random() < interim_asmt_rate:
        s.takes_interim_asmts = True

    return s


def generate_registration_system(year, extract_date, id_gen):
    """
    Generate a registration system.

    @param year: The academic year
    @param extract_date: The date of the data extract
    @param id_gen: ID generator
    @returns: The registration system
    """
    # Create the object
    ars = RegistrationSystem()
    ars.guid = id_gen.get_uuid()
    ars.sys_guid = id_gen.get_uuid()
    ars.academic_year = year
    ars.extract_date = extract_date
    ars.callback_url = 'SateTestReg.gov/StuReg/CallBack'

    return ars


def generate_institution_hierarchy(state: State, district: District, school: School, id_gen):
    """
    Generate a hierarchy institution object for a set of hierarchy institutions.

    @param state: The state in the hierarchy
    @param district: The district in the hierarchy
    @param school: The school in the hierarchy
    @param id_gen: ID generator
    @returns: An institution hierarchy object
    """
    # Create the object
    ih = InstitutionHierarchy()
    ih.rec_id = id_gen.get_rec_id('inst_hier')
    ih.guid = id_gen.get_uuid()
    ih.state = state
    ih.district = district
    ih.school = school
    ih.from_date = cfg.HIERARCHY_FROM_DATE
    ih.to_date = cfg.HIERARCHY_TO_DATE

    return ih


def sort_schools_by_grade(schools):
    """
    Sort a list of schools by grades available in the school.

    @param schools: Schools to sort
    @returns: Dictionary of sorted schools
    """
    schools_by_grade = {}
    for school in schools:
        for grade in school.grades:
            if grade not in schools_by_grade:
                schools_by_grade[grade] = []
            schools_by_grade[grade].append(school)
    return schools_by_grade


def set_up_schools_with_grades(schools, grades_of_concern):
    """
    Build a dictionary that associates each school with the grades of concern that a given school has.

    @param schools: Schools to set up
    @param grades_of_concern: The overall set of grades that we are concerned with
    @returns: Dictionary of schools to dictionary of grades
    """
    schools_with_grades = {}
    for school in schools:
        grades_for_school = grades_of_concern.intersection(school.config['grades'])
        schools_with_grades[school] = dict(zip(grades_for_school, [[] for _ in range(len(grades_for_school))]))
    return schools_with_grades
