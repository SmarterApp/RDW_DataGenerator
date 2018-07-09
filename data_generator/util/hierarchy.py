"""
This module provides utility functions for hierarchy operations.
"""

import csv
import random

import data_generator.config.hierarchy as hier_config
import data_generator.config.population as pop_config
import data_generator.config.state_types as state_config
import data_generator.generators.hierarchy as hier_gen
from data_generator.model.district import District
from data_generator.model.school import School
from data_generator.model.state import State
from data_generator.util.id_gen import IDGen

CsvFieldNames = [
    'state_id', 'state_code', 'state_name', 'state_type',
    'district_id', 'district_name', 'district_type',
    'school_id', 'school_name', 'school_type', 'school_interims'
]


def convert_config_school_count_to_ratios(config):
    """Take a district type hierarchy configuration and convert the school counts to decimal ratios. The configuration
    settings are manipulated in place.

    :param config: The district type configuration to manipulate
    """
    # Count the total number of schools that make up the ratio
    ratio_count = 0
    for st, count in config['school_types_and_ratios'].items():
        if count < 1:
            return  # This function has already been run on this configuration block
        ratio_count += count

    # Convert each count to decimal ratio
    for st, count in config['school_types_and_ratios'].items():
        config['school_types_and_ratios'][st] = count / ratio_count


def generate_hierarchy(type, name, code, id_gen: IDGen):
    state = hier_gen.generate_state(type, name, code, id_gen)
    districts = []
    schools = []
    for district_type, dist_type_count in state.config['district_types_and_counts']:
        for _ in range(dist_type_count):
            district = hier_gen.generate_district(district_type, state, id_gen)
            districts.append(district)

            # Create the schools for the district
            school_count = random.triangular(district.config['school_counts']['min'],
                                             district.config['school_counts']['max'],
                                             district.config['school_counts']['avg'])
            convert_config_school_count_to_ratios(district.config)
            for school_type, school_type_ratio in district.config['school_types_and_ratios'].items():
                school_type_count = max(int(school_count * school_type_ratio), 1)  # Make sure at least 1
                for _ in range(school_type_count):
                    school = hier_gen.generate_school(school_type, district, id_gen)
                    schools.append(school)

    return state, districts, schools


def write_hierarchy(file: str, schools: [School]):
    with open(file, "w") as f:
        writer = csv.DictWriter(f, CsvFieldNames)
        writer.writeheader()
        for school in schools:
            writer.writerow(_school_to_row(school))


def read_hierarchy(file: str) -> (State, [District], [School]):
    state = None
    districts = []
    schools = []

    district = None     # current district
    school = None
    with open(file) as f:
        reader = csv.DictReader(f)
        if len(set(CsvFieldNames).difference(reader.fieldnames)) > 0:
            raise ValueError("Invalid fieldnames, expected " + str(CsvFieldNames))

        for row in reader:
            old_state = state
            state, new_state = _extract_state(row, state)
            if old_state and new_state:
                raise ValueError("State mismatch, it must be the same for all rows")

            district, new_district = _extract_district(row, district, state)
            if new_district:
                districts.append(district)

            school, new_school = _extract_school(row, school, district)
            if new_school:
                schools.append(school)

    return state, districts, schools


def _school_to_row(school: School) -> dict:
    district = school.district
    state = district.state

    return {
        'state_id': state.id,
        'state_code': state.code,
        'state_name': state.name,
        'state_type': state.type_str,
        'district_id': district.id,
        'district_name': district.name,
        'district_type': district.type_str,
        'school_id': school.id,
        'school_name': school.name,
        'school_type': school.type_str,
        'school_interims': school.takes_interim_asmts
    }


def _extract_state(row: dict, cur: State) -> (State, bool):
    s = State()
    s.type_str = row['state_type']
    s.id = row['state_id']
    s.code = row['state_code']
    s.name = row['state_name']

    if cur and cur.type_str == s.type_str and cur.id == s.id and cur.code == s.code and cur.name == s.name:
        return cur, False

    if s.type_str not in state_config.STATE_TYPES:
        raise ValueError("State type '" + s.type_str + "' not found")

    s.config = state_config.STATE_TYPES[s.type_str]
    s.demo_config = pop_config.DEMOGRAPHICS[s.config['demographics']]
    s.guid = IDGen.get_uuid()

    return s, True


def _extract_district(row: dict, cur: District, state: State) -> (District, bool):
    d = District()
    d.type_str = row['district_type']
    d.id = row['district_id']
    d.name = row['district_name']

    if cur and cur.type_str == d.type_str and cur.id == d.id and cur.name == d.name:
        return cur, False

    if d.type_str not in hier_config.DISTRICT_TYPES:
        raise ValueError("District type '" + d.type_str + "' not found")

    d.config = hier_config.DISTRICT_TYPES[d.type_str]
    d.demo_config = state.demo_config
    d.state = state
    d.guid = IDGen.get_uuid()

    return d, True


def _extract_school(row: dict, cur: School, district: District) -> (School, bool):
    s = School()
    s.type_str = row['school_type']
    s.id = row['school_id']
    s.name = row['school_name']

    if cur and cur.type_str == s.type_str and cur.id == s.id and cur.name == s.name:
        return cur, False

    if s.type_str not in hier_config.SCHOOL_TYPES:
        raise ValueError("School type '" + s.type_str + "' not found")

    s.config = hier_config.SCHOOL_TYPES[s.type_str]
    s.demo_config = district.demo_config
    s.district = district
    s.guid = IDGen.get_uuid()
    s.takes_interim_asmts = str(row['school_interims']).lower() in ['1', 't', 'y', 'true', 'yes']

    return s, True
