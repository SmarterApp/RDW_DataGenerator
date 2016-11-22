"""
The data generator for the SBAC project.

Command line arguments:
  --team TEAM_NAME: Name of team to generate data for (expects sonics or arkanoids)
  --state_name STATE_NAME: Name of state to generate data for (defaults to 'North Carolina')
  --state_code STATE_CODE: Code of state to generate data for (defaults to 'NC')
  --state_type STATE_TYPE_NAME: Name of state type to generate data for (expects devel, typical_1, california)
  --pg_out: Output data to a PostgreSQL database
  --star_out: Output data to star schema CSV
  --lz_out: Output data to landing zone CSV and JSON

  If using PostgreSQL output:
    --host: Host for PostgreSQL server
    --schema: Schema for PostgreSQL database

@author: nestep
@date: March 17, 2014
"""

import argparse
import copy
import datetime
import itertools
import os
import random
import shutil

import data_generator.config.cfg as sbac_in_config
import data_generator.config.out as sbac_out_config
import data_generator.generators.iab_assessment as sbac_interim_asmt_gen
import data_generator.generators.summative_or_ica_assessment as sbac_asmt_gen
import data_generator.sbac_generators.hierarchy as sbac_hier_gen
import data_generator.sbac_generators.population as sbac_pop_gen
import data_generator.util.hiearchy as hier_util
import data_generator.writers.writecsv as csv_writer
import data_generator.writers.writejson as json_writer
import data_generator.writers.writepostgres as postgres_writer
from data_generator.sbac_model.summative_or_ica_assessmentoutcome import SBACAssessmentOutcome
from data_generator.sbac_model.district import SBACDistrict
from data_generator.sbac_model.institutionhierarchy import InstitutionHierarchy
from data_generator.sbac_model.state import SBACState
from data_generator.sbac_model.student import SBACStudent
from data_generator.util import all_combinations
from data_generator.util.id_gen import IDGen
from data_generator.writers.datefilters import FILTERS as DG_FILTERS
from data_generator.writers.filters import SBAC_FILTERS
from data_generator.sbac_model.summative_or_ica_assessment import SBACAssessment

OUT_PATH_ROOT = 'out'
DB_CONN = None
DB_SCHEMA = None

WRITE_STAR = False
WRITE_LZ = False
WRITE_PG = False
WRITE_IL = False

# See assign_team_configuration_options for these values
STATES = []
YEARS = []
ASMT_YEARS = []
INTERIM_ASMT_PERIODS = []
NUMBER_REGISTRATION_SYSTEMS = 1

# These are global regardless of team
GRADES_OF_CONCERN = {3, 4, 5, 6, 7, 8, 11}  # Made as a set for intersection later
REGISTRATION_SYSTEM_GUIDS = []
REGISTRATION_SYSTEMS = {}

# Register output filters
csv_writer.register_filters(SBAC_FILTERS)
postgres_writer.register_filters(SBAC_FILTERS)


def assign_configuration_options(gen_type, state_name, state_code, state_type):
    """
    Assign configuration options that are specific for the generation type

    @param gen_type: Generation run type to configure
    @param state_name: Name of state to generate
    @param state_code: Code of state to generate
    @param state_type: Type of state to generate
    """
    global STATES, YEARS, ASMT_YEARS, INTERIM_ASMT_PERIODS, NUMBER_REGISTRATION_SYSTEMS, WRITE_LZ, WRITE_STAR, \
        WRITE_PG, WRITE_IL, GRADES_OF_CONCERN

    # Validate parameter
    if gen_type not in ['regular', 'udl']:
        raise ValueError("Generation type '%s' is not known" % gen_type)

    # Set the state
    STATES = [{'name': state_name, 'code': state_code, 'type': state_type}]

    # Assign options
    if gen_type == 'regular':
        YEARS = [2015, 2016, 2017]  # Expected sorted lowest to highest
        ASMT_YEARS = [2015, 2016, 2017]  # The years to generate summative assessments for
        INTERIM_ASMT_PERIODS = ['Fall', 'Winter', 'Spring']  # The periods for interim assessments
        NUMBER_REGISTRATION_SYSTEMS = 1  # Should be less than the number of expected districts
    elif gen_type == 'udl':
        # This is a VERY specific configuration specifically designed to generate UDL test files
        STATES = [{'name': 'Example State', 'code': 'ES', 'type': 'udl_test'}]
        YEARS = [2016]
        ASMT_YEARS = [2016]
        INTERIM_ASMT_PERIODS = []
        NUMBER_REGISTRATION_SYSTEMS = 1
        GRADES_OF_CONCERN = {11}
        # sbac_in_config.SUBJECTS = ['Math']
        sbac_in_config.INTERIM_ASMT_RATE = 0
        sbac_in_config.ASMT_SKIP_RATE = 0
        sbac_in_config.ASMT_RETAKE_RATE = 0
        sbac_in_config.ASMT_DELETE_RATE = 0
        sbac_in_config.ASMT_UPDATE_RATE = 0
        WRITE_LZ = True
        WRITE_STAR = False
        WRITE_PG = False
        WRITE_IL = False


def connect_to_postgres(host, port, dbname, user, password):
    """
    Open a connection to PostgreSQL.

    @param host: Postgres server host
    @param port: Postgres server port
    @param dbname: Name of database to connect to
    @param user: Postgres server user
    @param password: Postgres server password
    """
    return postgres_writer.create_dbcon(host, port, dbname, user, password)


def prepare_output_files():
    """
    Prepare the star-schema output files before the data generation run begins creating data.
    """
    # Do not create files if we are not writing to star schema
    if not WRITE_STAR:
        return

    # Prepare star-schema output files
    csv_writer.prepare_csv_file(sbac_out_config.FAO_VW_FORMAT['name'],
                                sbac_out_config.FAO_VW_FORMAT['columns'],
                                root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.FAO_FORMAT['name'],
                                sbac_out_config.FAO_FORMAT['columns'],
                                root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.FBAO_FORMAT['name'],
                                sbac_out_config.FBAO_FORMAT['columns'],
                                root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.DIM_STUDENT_FORMAT['name'],
                                sbac_out_config.DIM_STUDENT_FORMAT['columns'],
                                root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.DIM_INST_HIER_FORMAT['name'],
                                sbac_out_config.DIM_INST_HIER_FORMAT['columns'],
                                root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.DIM_ASMT_FORMAT['name'],
                                sbac_out_config.DIM_ASMT_FORMAT['columns'],
                                root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.SR_FORMAT['name'],
                                sbac_out_config.SR_FORMAT['columns'],
                                root_path=OUT_PATH_ROOT)


def build_registration_systems(years, id_gen):
    """"
    Build the registration systems that will be used during the data generation run.

    @param years: The years for which data will be generated
    @param id_gen: ID generator
    @returns: A list of GUIDs for the registration systems that were created
    """
    # Validate years
    if len(years) == 0:
        raise ValueError('Number of specified years is zero')

    # Grab columns and layout for output files
    sr_out_cols = sbac_out_config.SR_FORMAT['columns']
    rs_out_layout = sbac_out_config.REGISTRATION_SYSTEM_FORMAT['layout']

    # Build the registration systems for every year
    guids = {}
    start_year = years[0] - 1
    for i in range(NUMBER_REGISTRATION_SYSTEMS):
        # Build the original system
        rs = sbac_hier_gen.generate_registration_system(start_year, str(start_year - 1) + '-02-25', id_gen)
        guids[rs.guid_sr] = {}

        # Update it over every year
        for year in YEARS:
            # Update the system
            rs.academic_year = year
            rs.extract_date = str(year - 1) + '-02-27'
            guids[rs.guid_sr][year] = copy.deepcopy(rs)

            # Write landing zone files if requested
            if WRITE_LZ:
                # Create the JSON file
                file_name = sbac_out_config.REGISTRATION_SYSTEM_FORMAT['name']
                file_name = file_name.replace('<YEAR>', str(year)).replace('<GUID>', rs.guid_sr)
                json_writer.write_object_to_file(file_name, rs_out_layout, rs, root_path=OUT_PATH_ROOT)

                # Prepare the SR CSV file
                file_name = sbac_out_config.SR_FORMAT['name'].replace('<YEAR>', str(year)).replace('<GUID>', rs.guid_sr)
                csv_writer.prepare_csv_file(file_name, sr_out_cols, root_path=OUT_PATH_ROOT)

    # Return the generated GUIDs
    return guids


def create_assessment_object(asmt_type, period, year, subject, id_gen, generate_item_level=True):
    """
    Create a new assessment object and write it out to JSON.

    @param asmt_type: Type of assessment to create
    @param period: Period (month) of assessment to create
    @param year: Year of assessment to create
    @param subject: Subject of assessment to create
    @param id_gen: ID generator
    @param generate_item_level: If sshould generate item-level data
    @returns: New assessment object
    """
    # Create assessment
    asmt = sbac_asmt_gen.generate_assessment(asmt_type, period, year, subject, id_gen,
                                             generate_item_level=generate_item_level)

    # Output to requested mediums
    if WRITE_LZ:
        file_name = sbac_out_config.ASMT_JSON_FORMAT['name'].replace('<GUID>', asmt.guid_sr)
        json_writer.write_object_to_file(file_name, sbac_out_config.ASMT_JSON_FORMAT['layout'], asmt,
                                         root_path=OUT_PATH_ROOT)
        file_name = sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<GUID>', asmt.guid_sr)
        csv_writer.prepare_csv_file(file_name, sbac_out_config.LZ_REALDATA_FORMAT['columns'], root_path=OUT_PATH_ROOT)

    if WRITE_STAR:
        file_name = sbac_out_config.DIM_ASMT_FORMAT['name']
        csv_writer.write_records_to_file(file_name, sbac_out_config.DIM_ASMT_FORMAT['columns'], [asmt],
                                         tbl_name='dim_asmt', root_path=OUT_PATH_ROOT)

    if WRITE_PG:
        postgres_writer.write_records_to_table(DB_CONN, DB_SCHEMA + '.dim_asmt',
                                               sbac_out_config.DIM_ASMT_FORMAT['columns'], [asmt])

    # Return the object
    return asmt


def create_interim_assessment_object(date: datetime.date,
                                     asmt_year: int,
                                     subject: str,
                                     block: str,
                                     grade: int,
                                     id_gen: IDGen,
                                     generate_item_level: bool = True):
    """
    Create a new assessment object and write it out to JSON.

    @:param date: date of the test
    @param asmt_year: Year of assessment to create
    @param subject: Subject of assessment to create
    @param block: block
    @param id_gen: ID generator
    @param generate_item_level: If sshould generate item-level data
    @returns: New assessment object
    """
    # Create assessment
    asmt = sbac_interim_asmt_gen.generate_interim_assessment(date, asmt_year, subject, block, grade, id_gen,
                                                             generate_item_level=generate_item_level)

    # Output to requested mediums
    if WRITE_LZ:
        file_name = sbac_out_config.IAB_JSON_FORMAT['name'].replace('<GUID>', asmt.guid_sr)
        json_writer.write_object_to_file(file_name, sbac_out_config.IAB_JSON_FORMAT['layout'], asmt,
                                         root_path=OUT_PATH_ROOT)
        file_name = sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<GUID>', asmt.guid_sr)
        csv_writer.prepare_csv_file(file_name, sbac_out_config.LZ_REALDATA_FORMAT['columns'], root_path=OUT_PATH_ROOT)

    if WRITE_STAR:
        file_name = sbac_out_config.DIM_ASMT_FORMAT['name']
        csv_writer.write_records_to_file(file_name, sbac_out_config.DIM_ASMT_FORMAT['columns'], [asmt],
                                         tbl_name='dim_asmt', root_path=OUT_PATH_ROOT)

    if WRITE_PG:
        postgres_writer.write_records_to_table(DB_CONN, DB_SCHEMA + '.dim_asmt',
                                               sbac_out_config.DIM_ASMT_FORMAT['columns'], [asmt])

    # Return the object
    return asmt


def create_assessment_outcome_object(student, asmt, inst_hier, id_gen, assessment_results,
                                     skip_rate=sbac_in_config.ASMT_SKIP_RATE,
                                     retake_rate=sbac_in_config.ASMT_RETAKE_RATE,
                                     delete_rate=sbac_in_config.ASMT_DELETE_RATE,
                                     update_rate=sbac_in_config.ASMT_UPDATE_RATE,
                                     generate_item_level=True):
    """
    Create the outcome(s) for a single assessment for a student. If the student is determined to have skipped the
    assessment, the resulting array will be empty. Otherwise, one outcome will be created with the chance that a second
    outcome is also created. A second outcome will be created if the assessment is re-taken or updated. If the
    assessment is determined to have been deleted, no second record will be created.

    @param student: The student to create an outcome for
    @param asmt: The assessment to create an outcome for
    @param inst_hier: The institution hierarchy this assessment relates to
    @param id_gen: ID generator
    @param assessment_results: Dictionary of assessment results to update
    @param skip_rate: The rate (chance) that this student skips the assessment
    @param retake_rate: The rate (chance) that this student will re-take the assessment
    @param delete_rate: The rate (chance) that this student's result will be deleted
    @param update_rate: The rate (chance) that this student's result will be updated (deleted and re-added)
    @param generate_item_level: If should generate item-level data
    @returns: Array of outcomes
    """
    # Make sure they are taking the assessment
    if random.random() < skip_rate:
        return

    # Make sure the assessment is known in the results
    if asmt.guid_sr not in assessment_results:
        assessment_results[asmt.guid_sr] = []

    # Create the original outcome object
    ao = sbac_asmt_gen.generate_assessment_outcome(student, asmt, inst_hier, id_gen,
                                                   generate_item_level=generate_item_level)
    assessment_results[asmt.guid_sr].append(ao)

    # Decide if something special is happening
    special_random = random.random()
    if special_random < retake_rate:
        # Set the original outcome object to inactive, create a new outcome (with an advanced date take), and return
        ao.result_status = sbac_in_config.ASMT_STATUS_INACTIVE
        ao2 = sbac_asmt_gen.generate_assessment_outcome(student, asmt, inst_hier, id_gen,
                                                        generate_item_level=generate_item_level)
        assessment_results[asmt.guid_sr].append(ao2)
        ao2.date_taken += datetime.timedelta(days=5)
    elif special_random < update_rate:
        # Set the original outcome object to deleted and create a new outcome
        ao.result_status = sbac_in_config.ASMT_STATUS_DELETED
        ao2 = sbac_asmt_gen.generate_assessment_outcome(student, asmt, inst_hier, id_gen,
                                                        generate_item_level=generate_item_level)
        assessment_results[asmt.guid_sr].append(ao2)

        # See if the updated record should be deleted
        if random.random() < delete_rate:
            ao2.result_status = sbac_in_config.ASMT_STATUS_DELETED
    elif special_random < delete_rate:
        # Set the original outcome object to deleted
        ao.result_status = sbac_in_config.ASMT_STATUS_DELETED


def create_assessment_outcome_objects(student, asmt_summ, interim_asmts, inst_hier, id_gen, assessment_results,
                                      skip_rate=sbac_in_config.ASMT_SKIP_RATE,
                                      retake_rate=sbac_in_config.ASMT_RETAKE_RATE,
                                      delete_rate=sbac_in_config.ASMT_DELETE_RATE,
                                      update_rate=sbac_in_config.ASMT_UPDATE_RATE,
                                      generate_item_level=True):
    """
    Create a set of assessment outcome object(s) for a student. If the student is determined to have skipped the
    assessment, the resulting array will be empty. Otherwise, one outcome will be created with the chance that a second
    outcome is also created. A second outcome will be created if the assessment is re-taken or updated. If the
    assessment is determined to have been deleted, no second record will be created.

    @param student: The student to create outcomes for
    @param asmt_summ: The summative assessment object
    @param interim_asmts: The interim assessment objects
    @param inst_hier: The institution hierarchy these assessments relate to
    @param id_gen: ID generator
    @param assessment_results: Dictionary of assessment results to update
    @param skip_rate: The rate (chance) that this student skips an assessment
    @param retake_rate: The rate (chance) that this student will re-take an assessment
    @param delete_rate: The rate (chance) that this student's result will be deleted
    @param update_rate: The rate (chance) that this student's result will be updated (deleted and re-added)
    @param generate_item_level: If should generate item-level data
    """
    # Create the summative assessment outcome
    create_assessment_outcome_object(student, asmt_summ, inst_hier, id_gen, assessment_results, skip_rate,
                                     retake_rate, delete_rate, update_rate, generate_item_level)

    # Generate interim assessment results (list will be empty if school does not perform
    # interim assessments)
    for asmt in interim_asmts:
        # Create the interim assessment outcome
        create_assessment_outcome_object(student, asmt, inst_hier, id_gen, assessment_results, skip_rate,
                                         retake_rate, delete_rate, update_rate, generate_item_level)


def create_iab_outcome_object(student: SBACStudent,
                              iab_asmt: SBACAssessment,
                              inst_hier: InstitutionHierarchy,
                              id_gen: IDGen,
                              iab_results: {str: SBACAssessmentOutcome},
                              generate_item_level=True):
    """

    :param student:
    :param iab_asmt:
    :param inst_hier:
    :param id_gen:
    :param iab_results:
    :param generate_item_level:
    :return:
    """
    # Make sure the assessment is known in the results
    if iab_asmt.guid_sr not in iab_results:
        iab_results[iab_asmt.guid_sr] = []

    # Create the original outcome object
    ao = sbac_interim_asmt_gen.generate_interim_assessment_outcome(student, iab_asmt, inst_hier, id_gen,
                                                                   generate_item_level=generate_item_level)
    iab_results[iab_asmt.guid_sr].append(ao)


def create_iab_outcome_objects(student: SBACStudent,
                               asmt_year: int,
                               grade: int,
                               subject: str,
                               asmts: {str: SBACAssessment},
                               inst_hier: InstitutionHierarchy,
                               id_gen: IDGen,
                               iab_results: {str: SBACAssessmentOutcome},
                               generate_item_level=True):
    """
    Create a set of interim assessment outcome objects for a student.

    :param student: The student to create outcomes for
    :param asmt_year:
    :param grade:
    :param subject:
    :param asmts: Relevant IAB assessments
    :param inst_hier: The institution hierarchy these assessments relate to
    :param id_gen: ID generator
    :param iab_results: Dictionary of iab results to update
    :param generate_item_level: If should generate item-level data
    :return: None
    """
    # for randomly selecting a subset of dates on which a student took the test
    date_combos = tuple(all_combinations(sbac_in_config.IAB_EFFECTIVE_DATES))

    for block in sbac_in_config.IAB_NAMES[subject][grade]:
        for offset_date in random.choice(date_combos):
            date = datetime.date(asmt_year + offset_date.year - 2, offset_date.month, offset_date.day)
            key = get_iab_key(date, grade, subject, block)
            iab_asmt = asmts[key]
            create_iab_outcome_object(student, iab_asmt, inst_hier, id_gen, iab_results,
                                      generate_item_level=generate_item_level)


def write_school_data(asmt_year, sr_out_name, dim_students, sr_students, assessment_results, iab_results, state_code,
                      district_id):
    """
    Write student and assessment data for a school to one or more output formats.

    @param asmt_year: Current academic year
    @param sr_out_name: Name of student registration landing zone CSV file to potentially write to
    @param dim_students: Students to write to dim_student star-schema CSVs/postgres tables
    @param sr_students: Students to write to registration landing zone/star-schema CSV/postgres table
    @param assessment_results: Assessment outcomes to write to landing zone/star-schema CSV/postgres table
    """
    # Set up output file names and columns
    sr_lz_out_cols = sbac_out_config.SR_FORMAT['columns']
    lz_asmt_out_cols = sbac_out_config.LZ_REALDATA_FORMAT['columns']
    it_lz_out_name = sbac_out_config.LZ_ITEMDATA_FORMAT['name']
    it_lz_out_cols = sbac_out_config.LZ_ITEMDATA_FORMAT['columns']
    fao_vw_out_name = sbac_out_config.FAO_VW_FORMAT['name']
    fao_vw_out_cols = sbac_out_config.FAO_VW_FORMAT['columns']
    fao_out_name = sbac_out_config.FAO_FORMAT['name']
    fao_out_cols = sbac_out_config.FAO_FORMAT['columns']
    fbao_out_name = sbac_out_config.FBAO_FORMAT['name']
    fbao_out_cols = sbac_out_config.FBAO_FORMAT['columns']
    dstu_out_name = sbac_out_config.DIM_STUDENT_FORMAT['name']
    dstu_out_cols = sbac_out_config.DIM_STUDENT_FORMAT['columns']
    sr_pg_out_name = sbac_out_config.STUDENT_REG_FORMAT['name']
    sr_pg_out_cols = sbac_out_config.STUDENT_REG_FORMAT['columns']

    # Write student data optionally to landing zone CSV, star-schema CSV, and/or to postgres
    if WRITE_LZ:
        csv_writer.write_records_to_file(sr_out_name, sr_lz_out_cols, sr_students, root_path=OUT_PATH_ROOT)

    if WRITE_STAR:
        csv_writer.write_records_to_file(dstu_out_name, dstu_out_cols, dim_students,
                                         entity_filter=('held_back', False), tbl_name='dim_student',
                                         root_path=OUT_PATH_ROOT)
        csv_writer.write_records_to_file(sr_pg_out_name, sr_pg_out_cols, sr_students, tbl_name='student_reg',
                                         root_path=OUT_PATH_ROOT)

    if WRITE_PG:
        postgres_writer.write_records_to_table(DB_CONN, DB_SCHEMA + '.dim_student', dstu_out_cols, dim_students,
                                               entity_filter=('held_back', False))
        postgres_writer.write_records_to_table(DB_CONN, DB_SCHEMA + '.student_reg', sr_pg_out_cols, sr_students)

    # Write assessment results if we have them; also optionally to landing zone CSV, star-schema CSV, and/or to postgres
    if asmt_year in ASMT_YEARS:
        for guid, rslts in iab_results.items():
            if WRITE_LZ:
                csv_writer.write_records_to_file(sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<GUID>', guid),
                                                 lz_asmt_out_cols,
                                                 rslts,
                                                 root_path=OUT_PATH_ROOT,
                                                 entity_filter=('result_status', 'C'))

            if WRITE_STAR:
                csv_writer.write_records_to_file(fbao_out_name, fbao_out_cols, rslts,
                                                 tbl_name='fact_block_asmt_outcome', root_path=OUT_PATH_ROOT)

            if WRITE_PG:
                try:
                    postgres_writer.write_records_to_table(DB_CONN, DB_SCHEMA + '.fact_block_asmt_outcome',
                                                           fbao_out_cols, rslts)
                except Exception as e:
                    print('PostgreSQL EXCEPTION ::: %s' % str(e))

        for guid, rslts in assessment_results.items():

            if WRITE_IL:
                for sao in rslts:
                    try:
                        asmt = sao.assessment
                        # Only write out summative item level results
                        if asmt.asmt_type == 'SUMMATIVE':
                            it_dir_path = os.path.join(state_code, str(asmt.period_year), asmt.asmt_type,
                                                       DG_FILTERS['date_Ymd'](asmt.effective_date), asmt.subject,
                                                       str(sao.student.grade), district_id)
                            it_file_path = os.path.join(it_dir_path, it_lz_out_name.replace('<STUDENT_ID>',
                                                                                            sao.student.guid_sr))

                            if not os.path.exists(os.path.join(OUT_PATH_ROOT, it_dir_path)):
                                os.makedirs(os.path.join(OUT_PATH_ROOT, it_dir_path))

                            csv_writer.write_records_to_file(it_file_path, it_lz_out_cols, sao.item_level_data,
                                                             root_path=OUT_PATH_ROOT)
                    finally:
                        pass

            if WRITE_LZ:
                csv_writer.write_records_to_file(sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<GUID>', guid),
                                                 lz_asmt_out_cols, rslts, root_path=OUT_PATH_ROOT,
                                                 entity_filter=('result_status', 'C'))
            if WRITE_STAR:
                csv_writer.write_records_to_file(fao_vw_out_name, fao_vw_out_cols, rslts,
                                                 tbl_name='fact_asmt_outcome_vw', root_path=OUT_PATH_ROOT)
                csv_writer.write_records_to_file(fao_out_name, fao_out_cols, rslts,
                                                 tbl_name='fact_asmt_outcome', root_path=OUT_PATH_ROOT)
            if WRITE_PG:
                try:
                    postgres_writer.write_records_to_table(DB_CONN, DB_SCHEMA + '.fact_asmt_outcome_vw',
                                                           fao_vw_out_cols, rslts)
                    postgres_writer.write_records_to_table(DB_CONN, DB_SCHEMA + '.fact_asmt_outcome',
                                                           fao_out_cols, rslts)
                except Exception as e:
                    print('PostgreSQL EXCEPTION ::: %s' % str(e))


def generate_district_data(state: SBACState,
                           district: SBACDistrict,
                           reg_sys_guid: str,
                           assessments: {str: SBACAssessment},
                           asmt_skip_rates_by_subject: {str: float},
                           id_gen: IDGen):
    """
    Generate an entire data set for a single district.

    @param state: State the district belongs to
    @param district: District to generate data for
    @param reg_sys_guid: GUID for registration system this district is assigned to
    @param assessments: Dictionary of all assessment objects
    @param asmt_skip_rates_by_subject: The rate that students skip a given assessment
    @param id_gen: ID generator
    """
    # Grab the registration system
    reg_sys = REGISTRATION_SYSTEMS[reg_sys_guid]

    # Decide how many schools to make
    school_count = random.triangular(district.config['school_counts']['min'],
                                     district.config['school_counts']['max'],
                                     district.config['school_counts']['avg'])

    # Convert school type counts into decimal ratios
    hier_util.convert_config_school_count_to_ratios(district.config)

    # Make the schools
    hierarchies = []
    inst_hiers = {}
    schools = []

    for school_type, school_type_ratio in district.config['school_types_and_ratios'].items():
        # Decide how many of this school type we need
        school_type_count = max(int(school_count * school_type_ratio), 1)  # Make sure at least 1

        for j in range(school_type_count):
            # Create the school and institution hierarchy object
            school = sbac_hier_gen.generate_school(school_type, district, id_gen)
            ih = sbac_hier_gen.generate_institution_hierarchy(state, district, school, id_gen)
            hierarchies.append(ih)
            inst_hiers[school.guid] = ih
            schools.append(school)

    # Write out hierarchies for this district
    if WRITE_STAR:
        csv_writer.write_records_to_file(sbac_out_config.DIM_INST_HIER_FORMAT['name'],
                                         sbac_out_config.DIM_INST_HIER_FORMAT['columns'], hierarchies,
                                         tbl_name='dim_hier', root_path=OUT_PATH_ROOT)

    if WRITE_PG:
        postgres_writer.write_records_to_table(DB_CONN, DB_SCHEMA + '.dim_inst_hier',
                                               sbac_out_config.DIM_INST_HIER_FORMAT['columns'], hierarchies)

    # Sort the schools
    schools_by_grade = sbac_hier_gen.sort_schools_by_grade(schools)

    # Student grouping is enabled for district using Student_grouping_rate
    if district.student_grouping:
        schools_with_groupings = sbac_hier_gen.set_up_schools_with_groupings(schools, GRADES_OF_CONCERN)
        pop_schools_with_groupings = sbac_hier_gen.populate_schools_with_groupings(schools_with_groupings, id_gen)

    # Begin processing the years for data
    unique_students = {}
    students = {}
    student_count = 0
    for asmt_year in YEARS:
        # Prepare output file names
        rg_sys_year = reg_sys[asmt_year]
        rg_guid = rg_sys_year.guid_sr
        sr_out_name = sbac_out_config.SR_FORMAT['name'].replace('<YEAR>', str(asmt_year)).replace('<GUID>', rg_guid)

        # Set up a dictionary of schools and their grades
        schools_with_grades = sbac_hier_gen.set_up_schools_with_grades(schools, GRADES_OF_CONCERN)

        # Advance the students forward in the grades
        for guid, student in students.items():
            # Assign the registration system and bump up the record ID
            student.reg_sys = rg_sys_year
            student.rec_id_sr = id_gen.get_rec_id('sr_student')

            # Move the student forward (false from the advance method means the student disappears)
            if sbac_pop_gen.advance_student(student, schools_by_grade):
                schools_with_grades[student.school][student.grade].append(student)

        # With the students moved around, we will re-populate empty grades and create assessments with outcomes for
        # the students
        for school, grades in schools_with_grades.items():
            # Get the institution hierarchy object
            inst_hier = inst_hiers[school.guid]

            # Process the whole school
            assessment_results = {}
            iab_results = {}
            sr_students = []
            dim_students = []
            for grade, grade_students in grades.items():
                # Potentially re-populate the student population
                sbac_pop_gen.repopulate_school_grade(school, grade, grade_students, id_gen, state, rg_sys_year,
                                                     asmt_year)
                student_count += len(grade_students)

                if district.student_grouping:
                    sbac_pop_gen.assign_student_groups(school, grade, grade_students, pop_schools_with_groupings)

                # Create assessment results for this year if requested
                if asmt_year in ASMT_YEARS:
                    first_subject = True
                    for subject in sbac_in_config.SUBJECTS:
                        # Get the subject skip rate
                        skip_rate = asmt_skip_rates_by_subject[subject]

                        # Grab the summative assessment object
                        asmt_summ = assessments[str(asmt_year) + 'summative' + str(grade) + subject]

                        # Grab the interim assessment objects
                        interim_asmts = []
                        if school.takes_interim_asmts:
                            for period in INTERIM_ASMT_PERIODS:
                                key = str(asmt_year) + 'interim' + period + str(grade) + subject
                                interim_asmts.append(assessments[key])

                        for student in grade_students:
                            # Create the outcome(s)
                            create_assessment_outcome_objects(student, asmt_summ, interim_asmts, inst_hier, id_gen,
                                                              assessment_results, skip_rate,
                                                              generate_item_level=WRITE_IL)

                            if not student.skip_iab:
                                create_iab_outcome_objects(student,
                                                           asmt_year,
                                                           grade,
                                                           subject,
                                                           assessments,
                                                           inst_hier,
                                                           id_gen,
                                                           iab_results,
                                                           generate_item_level=WRITE_IL)

                            # Determine if this student should be in the SR file
                            if random.random() < sbac_in_config.HAS_ASMT_RESULT_IN_SR_FILE_RATE and first_subject:
                                sr_students.append(student)

                            # Make sure we have the student for the next run
                            if student.guid not in students:
                                students[student.guid] = student
                                dim_students.append(student)

                            if student.guid not in unique_students:
                                unique_students[student.guid] = True

                        first_subject = False

                else:
                    # We're not doing assessment results, so put all of the students into the list
                    sr_students.extend(grade_students)
                    for student in grade_students:
                        if student.guid not in students:
                            students[student.guid] = student
                            dim_students.append(student)
                        if student.guid not in unique_students:
                            unique_students[student.guid] = True

            # Write out the school
            write_school_data(asmt_year, sr_out_name, dim_students, sr_students, assessment_results, iab_results,
                              state.code, district.guid)

            del dim_students
            del sr_students
            del assessment_results
            del iab_results

    unique_student_count = len(unique_students)

    # Some explicit garbage collection
    del hierarchies
    del inst_hiers
    del schools
    del schools_by_grade
    del students
    del unique_students

    # Return the average student count
    return int(student_count // len(ASMT_YEARS)), unique_student_count


def get_iab_key(date, grade, subject, block):
    return "%i-%i-%i IAB %i %s %s" % (date.year, date.month, date.day, grade, subject, block)


def generate_state_data(state: SBACState,
                        id_gen: IDGen,
                        generate_iabs: bool):
    """
    Generate an entire data set for a single state.

    @param state: State to generate data for
    @param id_gen: ID generator
    """
    # Grab the assessment rates by subjects
    asmt_skip_rates_by_subject = state.config['subject_skip_percentages']

    # Create the assessment objects
    assessments = {}

    if generate_iabs:
        for subject, grade in itertools.product(sbac_in_config.SUBJECTS,
                                                GRADES_OF_CONCERN):

            for year, block, offset_date in itertools.product(ASMT_YEARS,
                                                              sbac_in_config.IAB_NAMES[subject][grade],
                                                              sbac_in_config.IAB_EFFECTIVE_DATES, ):
                date = datetime.date(year + offset_date.year - 2, offset_date.month, offset_date.day)
                key = get_iab_key(date, grade, subject, block)

                assessments[key] = create_interim_assessment_object(date, year, subject, block, grade,
                                                                    id_gen, generate_item_level=WRITE_IL)

    for year in ASMT_YEARS:
        for subject in sbac_in_config.SUBJECTS:
            for grade in GRADES_OF_CONCERN:
                # Create the summative assessment
                asmt_key_summ = str(year) + 'summative' + str(grade) + subject
                assessments[asmt_key_summ] = create_assessment_object('SUMMATIVE', 'Spring', year, subject,
                                                                      id_gen, generate_item_level=WRITE_IL)

                # Create the interim assessments
                for period in INTERIM_ASMT_PERIODS:
                    asmt_key_intrm = str(year) + 'interim' + period + str(grade) + subject
                    asmt_intrm = create_assessment_object('INTERIM COMPREHENSIVE', period, year, subject,
                                                          id_gen, generate_item_level=WRITE_IL)
                    assessments[asmt_key_intrm] = asmt_intrm

    # Build the districts
    student_avg_count = 0
    student_unique_count = 0
    for district_type, dist_type_count in state.config['district_types_and_counts']:
        for _ in range(dist_type_count):
            # Create the district
            district = sbac_hier_gen.generate_district(district_type, state, id_gen)
            print('  Creating District: %s (%s District)' % (district.name, district.type_str))

            # Generate the district data set
            avg_year, unique = generate_district_data(state, district, random.choice(REGISTRATION_SYSTEM_GUIDS),
                                                      assessments, asmt_skip_rates_by_subject, id_gen)

            # Print completion of district
            print('    District created with average of %i students/year and %i total unique' % (avg_year, unique))
            student_avg_count += avg_year
            student_unique_count += unique

    # Print completion of state
    print('State %s created with average of %i students/year and %i total unique' % (state.name, student_avg_count,
                                                                                     student_unique_count))


if __name__ == '__main__':
    # Argument parsing for task-specific arguments
    parser = argparse.ArgumentParser(description='SBAC data generation task.')
    # udl overrides other settings
    parser.add_argument('-t', '--type', dest='gen_type', action='store', default='regular',
                        help='Specify the type of data generation run to perform (regular, udl)',
                        required=False)
    parser.add_argument('-sn', '--state_name', dest='state_name', action='store', default='California',
                        help='Specify the name of the state to generate data for (default=California)',
                        required=False)
    parser.add_argument('-sc', '--state_code', dest='state_code', action='store', default='CA',
                        help='Specify the code of the state to generate data for (default=CA)',
                        required=False)
    parser.add_argument('-st', '--state_type', dest='state_type', action='store', default='devel',
                        help='Specify the type of state to generate data for (devel (default), typical_1, california, udl_test)',
                        required=False)
    parser.add_argument('-o', '--out_dir', dest='out_dir', action='store', default='out',
                        help='Specify the root directory for writing output files to (default=%(default)s)',
                        required=False)
    parser.add_argument('-ho', '--host', dest='pg_host', action='store', default='localhost',
                        help='The host for the PostgreSQL server to write data to')
    parser.add_argument('-pa', '--pass', dest='pg_pass', action='store', default='',
                        help='The password for the PostgreSQL server to write data to')
    parser.add_argument('-s', '--schema', dest='pg_schema', action='store', default='dg_data',
                        help='The schema for the PostgreSQL database to write data to')
    parser.add_argument('-po', '--pg_out', dest='pg_out', action='store_true',
                        help='Output data to PostgreSQL database', required=False)
    parser.add_argument('-so', '--star_out', dest='star_out', action='store_true',
                        help='Output data to star schema CSV', required=False)
    parser.add_argument('-lo', '--lz_out', dest='lz_out', action='store_true',
                        help='Output data to landing zone CSV and JSON', required=False)
    parser.add_argument('-io', '--il_out', dest='il_out', action='store_true', help='Output item-level data',
                        required=False)
    parser.add_argument('-gia', '--generate_iabs', dest='generate_iabs',
                        action='store_false', default=True,
                        help='generate interim assessment blocks (default=%(default)s)')
    args, unknown = parser.parse_known_args()

    # Save output flags
    WRITE_PG = args.pg_out
    WRITE_STAR = args.star_out
    WRITE_LZ = args.lz_out
    WRITE_IL = args.il_out

    # Save output directory
    OUT_PATH_ROOT = args.out_dir

    # Set team-specific configuration options
    assign_configuration_options(args.gen_type, args.state_name, args.state_code, args.state_type)

    # Validate at least one form of output
    if not WRITE_PG and not WRITE_STAR and not WRITE_LZ:
        print('Please specify at least one output format')
        print('  --pg_out    Output to PostgreSQL')
        print('  --star_out  Output star schema CSV')
        print('  --lz_out    Output landing zone CSV and JSON')
        exit()

    # Record current (start) time
    tstart = datetime.datetime.now()

    # Verify output directory exists
    if not os.path.exists(OUT_PATH_ROOT):
        os.makedirs(OUT_PATH_ROOT)

    # Clean output directory
    for file in os.listdir(OUT_PATH_ROOT):
        file_path = os.path.join(OUT_PATH_ROOT, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except:
            pass

    # Connect to Postgres
    if WRITE_PG:
        DB_CONN = connect_to_postgres(args.pg_host, 5432, 'edware', 'edware', args.pg_pass)
        DB_SCHEMA = args.pg_schema

    # Create the ID generator
    idg = IDGen()

    # Prepare the output files
    prepare_output_files()

    # Create the registration systems
    REGISTRATION_SYSTEMS = build_registration_systems(YEARS, idg)
    for guid, _ in REGISTRATION_SYSTEMS.items():
        REGISTRATION_SYSTEM_GUIDS.append(guid)

    # Start the generation of data
    for state_cfg in STATES:
        # Create the state object
        state = sbac_hier_gen.generate_state(state_cfg['type'], state_cfg['name'], state_cfg['code'], idg)
        print()
        print('Creating State: %s' % state.name)

        # Process the state
        generate_state_data(state, idg, generate_iabs=args.generate_iabs)

    # Close the open DB connection
    if WRITE_PG:
        DB_CONN.close()

    # Record now current (end) time
    tend = datetime.datetime.now()

    # Print statistics
    print()
    print('Run began at:  %s' % tstart)
    print('Run ended at:  %s' % tend)
    print('Run run took:  %s' % (tend - tstart))
    print()
