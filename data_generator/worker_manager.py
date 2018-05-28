import copy
import datetime
import itertools
import json
import os
import random
import sys

import pyprind

import data_generator.config.cfg as cfg
import data_generator.generators.hierarchy as hier_gen
import data_generator.generators.iab_assessment as iab_asmt_gen
import data_generator.generators.population as pop_gen
import data_generator.generators.summative_or_ica_assessment as asmt_gen
import data_generator.util.hiearchy as hier_util
from data_generator.model.assessment import Assessment
from data_generator.model.district import District
from data_generator.model.registrationsystem import RegistrationSystem
from data_generator.model.state import State
from data_generator.outputworkers.csv_item_level_data_worker import CSVItemLevelDataWorker
from data_generator.outputworkers.csv_star_worker import CSVStarWorker
from data_generator.outputworkers.lz_worker import LzWorker
from data_generator.outputworkers.pg_worker import PgWorker
from data_generator.outputworkers.worker import Worker
from data_generator.outputworkers.xml_worker import XmlWorker
from data_generator.readers.tabulator_reader import load_assessments
from data_generator.util.id_gen import IDGen

# constants used when generating assessment packages
ASMT_YEARS = [2015, 2016, 2017]  # Expected sorted lowest to highest
INTERIM_ASMT_PERIODS = ['Fall', 'Winter', 'Spring']  # The periods for interim assessments

# These are global regardless of team
GRADES_OF_CONCERN = {3, 4, 5, 6, 7, 8, 11}  # Made as a set for intersection later


class WorkerManager(Worker):
    def __init__(self, args):
        self._args = args

        # Save output directory
        self.out_path_root = args.out_dir
        self.state_cfg = {'name': args.state_name, 'code': args.state_code, 'type': args.state_type}

        # Set up output
        self.workers = []
        if args.pg_out:
            self.workers.append(PgWorker(args.pg_host, 5432, 'edware', 'edware', args.pg_pass, args.pg_schema))
        if args.star_out:
            self.workers.append(CSVStarWorker(self.out_path_root))
            if args.gen_item:
                self.workers.append(CSVItemLevelDataWorker(self.out_path_root))
        if args.lz_out:
            self.workers.append(LzWorker(self.out_path_root))
        if args.xml_out:
            self.workers.append(XmlWorker(self.out_path_root))

        # assessment package settings
        self.pkg_source = args.pkg_source
        self.sum_pkg = args.sum_pkg
        self.ica_pkg = args.ica_pkg
        self.iab_pkg = args.iab_pkg
        self.gen_sum = args.gen_sum
        self.gen_ica = args.gen_ica
        self.gen_iab = args.gen_iab
        self.gen_item = args.gen_item

        self.org_source = args.org_source

        self.id_gen = IDGen()

    def cleanup(self):
        for worker in self.workers:
            worker.cleanup()

    def prepare(self):
        for worker in self.workers:
            worker.prepare()

    def run(self):
        state = hier_gen.generate_state(self.state_cfg['type'], self.state_cfg['name'], self.state_cfg['code'], self.id_gen)
        print('Creating State: %s' % state.name)

        assessments = self.__assessment_packages()

        if len(assessments) == 0:
            print('No assessment packages found')
            return

        # Process the state
        self.__load_external_organizations()
        self.__generate_state_data(state, assessments)

    def __assessment_packages(self):
        """
        Generate or load assessment packages based on settings
        
        :return: [Assessment]
        """
        assessments = []

        if self.pkg_source == 'generate':
            assessments.extend(self.__generate_assessments())
            for worker in self.workers:
                worker.write_assessments(assessments)
        else:
            assessments.extend(load_assessments(self.pkg_source, self.sum_pkg, self.ica_pkg, self.iab_pkg, self.gen_item))

        return assessments

    def __years(self, assessments: [Assessment]):
        """
        Return the sorted list of years represented by assessment packages.
        :param assessments: assessments 
        :return: sorted list of years, e.g. [2015, 2016, 2017]
        """
        return sorted(set(map(lambda asmt: asmt.year, assessments)))

    def __load_external_organizations(self):
        """
        Look for an organizations.json file and load any contents
        """
        file = os.path.join(self.org_source, 'organizations.json')
        if os.path.isfile(file):
            with open(file, "r") as f:
                org = json.load(f)
                if 'districts' in org: cfg.EXTERNAL_DISTRICTS = {d['entityId']: d for d in org['districts']}
                if 'institutions' in org: cfg.EXTERNAL_SCHOOLS = {s['entityId']: s for s in org['institutions']}
            print('Loaded external organizations, %d districts, %d schools' % (len(cfg.EXTERNAL_DISTRICTS), len(cfg.EXTERNAL_SCHOOLS)))

    def __generate_state_data(self, state: State, assessments: [Assessment]):
        """
        Generate an entire data set for a single state.

        @param state: State to generate data for
        """

        # build registration system by years
        rs_by_year = self.__build_registration_system(self.__years(assessments))

        # Build the districts
        student_avg_count = 0
        student_unique_count = 0
        for district_type, dist_type_count in state.config['district_types_and_counts']:
            for _ in range(dist_type_count):
                # Create the district
                district = hier_gen.generate_district(district_type, state, self.id_gen)
                print('\nCreating District: %s (%s District)' % (district.name, district.type_str))

                # Generate the district data set
                avg_year, unique = self.__generate_district_data(state, district, rs_by_year, assessments)

                # Print completion of district
                print('District created with average of %i students/year and %i total unique' % (avg_year, unique))
                student_avg_count += avg_year
                student_unique_count += unique

        # Print completion of state
        print('State %s created with average of %i students/year and %i total unique' % (state.name, student_avg_count, student_unique_count))

    def __generate_assessments(self):
        """
        :return: generate assessments
        """
        assessments = []

        if not (self.sum_pkg or self.ica_pkg or self.iab_pkg):
            return assessments

        # set up a progress bar
        progress_max = len(ASMT_YEARS) * len(cfg.SUBJECTS) * len(GRADES_OF_CONCERN)
        bar = pyprind.ProgBar(progress_max, stream=sys.stdout, title='Generating Assessments')

        for year, subject, grade in itertools.product(ASMT_YEARS, cfg.SUBJECTS, GRADES_OF_CONCERN):
            if self.sum_pkg:
                assessments.append(self.__create_and_write_assessment('SUMMATIVE', 'Spring', year, subject, grade))
            if self.ica_pkg:
                for period in INTERIM_ASMT_PERIODS:
                    assessments.append(self.__create_and_write_assessment('INTERIM COMPREHENSIVE', period, year, subject, grade))
            if self.iab_pkg:
                for block in cfg.IAB_NAMES[subject][grade]:
                    assessments.append(self.__create_and_write_iab_assessment(block, year, subject, grade))
            bar.update()

        return assessments

    def __create_and_write_iab_assessment(self, block, year, subject, grade):
        asmt = iab_asmt_gen.generate_interim_assessment(year, subject, block, grade, self.id_gen, gen_item=self.gen_item)
        for worker in self.workers:
            worker.write_iab(asmt)
        return asmt

    def __create_and_write_assessment(self, type, period, year, subject, grade):
        asmt = asmt_gen.generate_assessment(type, period, year, subject, grade, self.id_gen, gen_item=self.gen_item)
        for worker in self.workers:
            worker.write_assessment(asmt)
        return asmt

    def __build_registration_system(self, years):
        """"
        Build the registration system that will be used during the data generation run.

        @param years: The years for which data will be generated
        @returns: A list of year for the registration systems that was created
        """
        # Validate years
        if len(years) == 0:
            raise ValueError('Number of specified years is zero')

        # Build the registration systems for every year
        rs_by_year = {}
        start_year = years[0] - 1
        # Build the original system
        rs = hier_gen.generate_registration_system(start_year, str(start_year - 1) + '-02-25', self.id_gen)

        # Update it over every year
        for year in years:
            # Update the system
            rs.academic_year = year
            rs.extract_date = str(year - 1) + '-02-27'
            rs_by_year[year] = copy.deepcopy(rs)

            for worker in self.workers:
                worker.write_student_registration_config(year, rs)

        # Return the generated GUIDs
        return rs_by_year

    def __generate_institution_hierarchy(self, state: State, district: District, inst_hiers, schools):
        school_count = random.triangular(district.config['school_counts']['min'],
                                         district.config['school_counts']['max'],
                                         district.config['school_counts']['avg'])

        # Convert school type counts into decimal ratios
        hier_util.convert_config_school_count_to_ratios(district.config)

        # Make the schools
        hierarchies = []

        for school_type, school_type_ratio in district.config['school_types_and_ratios'].items():
            # Decide how many of this school type we need
            school_type_count = max(int(school_count * school_type_ratio), 1)  # Make sure at least 1

            for j in range(school_type_count):
                # Create the school and institution hierarchy object
                school = hier_gen.generate_school(school_type, district, self.id_gen)
                ih = hier_gen.generate_institution_hierarchy(state, district, school, self.id_gen)
                hierarchies.append(ih)
                inst_hiers[school.guid] = ih
                schools.append(school)

        # Write out hierarchies for this district
        for worker in self.workers:
            worker.write_hierarchies(hierarchies)

        # Some explicit garbage collection
        del hierarchies

    def __generate_district_data(self, state: State, district: District, reg_sys_by_year: {str: RegistrationSystem}, assessments: [Assessment]):
        """
        Generate an entire data set for a single district.

        @param state: State the district belongs to
        @param district: District to generate data for
        @param assessments: Dictionary of all assessment objects
        """
        inst_hiers = {}
        schools = []
        # Make the schools
        self.__generate_institution_hierarchy(state, district, inst_hiers, schools)

        # Sort the schools
        schools_by_grade = hier_gen.sort_schools_by_grade(schools)

        # Begin processing the years for data
        unique_students = {}
        students = {}
        student_count = 0

        # get range of years from assessment packages
        years = self.__years(assessments)

        # calculate the progress bar max and start the progress
        progress_max = len(hier_gen.set_up_schools_with_grades(schools, GRADES_OF_CONCERN)) * len(years)
        bar = pyprind.ProgBar(progress_max, stream=sys.stdout, title='Generating assessments outcome for schools')

        for year in years:
            # Prepare output file names
            reg_system = reg_sys_by_year[year]

            # Set up a dictionary of schools and their grades
            schools_with_grades = hier_gen.set_up_schools_with_grades(schools, GRADES_OF_CONCERN)

            # Advance the students forward in the grades
            for guid, student in students.items():
                # Assign the registration system and bump up the record ID
                student.reg_sys = reg_system
                student.rec_id = self.id_gen.get_rec_id('student')

                # Move the student forward (false from the advance method means the student disappears)
                if pop_gen.advance_student(student, schools_by_grade):
                    schools_with_grades[student.school][student.grade].append(student)

            # With the students moved around, we will re-populate empty grades
            # and create assessments with outcomes for the students
            for school, grades in schools_with_grades.items():
                # Process the whole school
                student_count += self.__process_school(grades, school, students, unique_students, state, district,
                                                       reg_system, year, inst_hiers[school.guid], assessments)
                bar.update()

        unique_student_count = len(unique_students)

        # Some explicit garbage collection
        del inst_hiers
        del schools
        del schools_by_grade
        del students
        del unique_students

        # Return the average student count
        return int(student_count // len(years)), unique_student_count

    def __process_school(self, grades, school, students, unique_students, state, district, reg_system: RegistrationSystem,
                         year, inst_hier, assessments):

        # Grab the assessment rates by subjects
        asmt_skip_rates_by_subject = state.config['subject_skip_percentages']

        # Process the whole school
        assessment_results = {}
        iab_results = {}
        sr_students = []
        dim_students = []
        student_count = 0

        for grade, grade_students in grades.items():
            # Potentially re-populate the student population
            pop_gen.repopulate_school_grade(school, grade, grade_students, self.id_gen, reg_system, year)
            student_count += len(grade_students)

            pop_gen.assign_student_groups(school, grade, grade_students, self.id_gen)

            # collect any assessments for this year and grade
            asmts = list(filter(lambda asmt: asmt.year == year and asmt.grade == grade, assessments))

            # collect students, generating assessments as appropriate
            for student in grade_students:
                for asmt in asmts:
                    if 'block' in asmt.type.lower():
                        for offset_date in cfg.IAB_EFFECTIVE_DATES:
                            date_taken = datetime.date(year + offset_date.year - 2, offset_date.month, offset_date.day)
                            iab_asmt_gen.create_iab_outcome_object(date_taken, student, asmt, inst_hier,
                                                                   self.id_gen, iab_results, gen_item=self.gen_item)
                    else:
                        asmt_gen.create_assessment_outcome_object(student, asmt, inst_hier, self.id_gen,
                                                                  assessment_results, asmt_skip_rates_by_subject[asmt.subject], gen_item=self.gen_item)

                if student.guid not in students:
                    students[student.guid] = student
                    dim_students.append(student)
                if student.guid not in unique_students:
                    unique_students[student.guid] = True
                # if no assessments were generated for this student, always add to SR file
                # otherwise, randomly allow some students to not be added (not really sure why this logic)
                if len(asmts) == 0 or (random.random() < cfg.HAS_ASMT_RESULT_IN_SR_FILE_RATE):
                    sr_students.append(student)

        # Write out the school
        self.__write_school_data(year, reg_system.guid, dim_students, sr_students, assessment_results, iab_results, state.code, district.guid)

        del dim_students
        del sr_students
        del assessment_results
        del iab_results

        return student_count

    def __write_school_data(self, year, rs_guid, dim_students, sr_students, assessment_results, iab_results, state_code, district_id):
        """
        Write student and assessment data for a school to one or more output formats.

        @param year: Current academic year
        @param dim_students: Students to write to dim_student star-schema CSVs/postgres tables
        @param sr_students: Students to write to registration landing zone/star-schema CSV/postgres table
        @param assessment_results: Assessment outcomes to write to landing zone/star-schema CSV/postgres table
        @param iab_results: IAB assessment outcomes
        @param state_code: state code
        @param district_id: district it
        """

        for worker in self.workers:
            worker.write_students_dim(dim_students)
            worker.write_students_reg(sr_students, rs_guid, year)

        # Write assessment results if we have them
        for guid, iab_result in iab_results.items():
            for worker in self.workers:
                worker.write_iab_outcome(iab_result, guid)
        for guid, results in assessment_results.items():
            for worker in self.workers:
                worker.write_assessment_outcome(results, guid, state_code, district_id)
