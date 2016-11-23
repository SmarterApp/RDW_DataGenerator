import copy
import datetime
import itertools
import os
import random
import sys

import data_generator.config.cfg as sbac_in_config
import data_generator.config.out as sbac_out_config
import data_generator.generators.iab_assessment as sbac_interim_asmt_gen
import data_generator.generators.summative_or_ica_assessment as sbac_asmt_gen
import data_generator.sbac_generators.hierarchy as sbac_hier_gen
import data_generator.sbac_generators.population as sbac_pop_gen
import data_generator.util.hiearchy as hier_util
import data_generator.writers.writecsv as csv_writer
import pyprind
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.district import District
from data_generator.model.interimassessment import InterimAssessment
from data_generator.model.registrationsystem import RegistrationSystem
from data_generator.model.state import State
from data_generator.outputworkers.csv_star_worker import CSVStarWorker
from data_generator.outputworkers.lz_worker import LzWorker
from data_generator.outputworkers.pg_worker import PgWorker
from data_generator.outputworkers.worker import Worker
from data_generator.util.id_gen import IDGen
from data_generator.writers.datefilters import FILTERS as DG_FILTERS

YEARS = [2015, 2016, 2017]  # Student registration years, expected sorted lowest to highest
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

        # Save output flags
        self.workers = []
        if args.pg_out:
            self.workers.append(PgWorker(args.pg_host, 5432, 'edware', 'edware', args.pg_pass, args.pg_schema))
        if args.star_out:
            self.workers.append(CSVStarWorker(self.out_path_root))
        if args.lz_out:
            self.workers.append(LzWorker(self.out_path_root))

        self.generate_iabs = args.generate_iabs
        self.generate_item_level = args.il_out
        self.id_gen = IDGen()

        for worker in self.workers:
            worker.prepare()

    def cleanup(self):
        for worker in self.workers:
            worker.cleanup()

    def run(self):
        state = sbac_hier_gen.generate_state(self.state_cfg['type'], self.state_cfg['name'], self.state_cfg['code'], self.id_gen)
        print('Creating State: %s' % state.name)

        # Process the state
        self.__generate_state_data(state)

    def __generate_state_data(self, state: State):
        """
        Generate an entire data set for a single state.

        @param state: State to generate data for
        """

        # build registration system by years
        rs_by_year = self.__build_registration_system()

        # Create the assessment objects
        assessments = {}

        if self.generate_iabs:
            assessments.update(self.__generate_iabs())

        assessments.update(self.__generate_assessments())

        # Build the districts
        student_avg_count = 0
        student_unique_count = 0
        for district_type, dist_type_count in state.config['district_types_and_counts']:
            for _ in range(dist_type_count):
                # Create the district
                district = sbac_hier_gen.generate_district(district_type, state, self.id_gen)
                print('\nCreating District: %s (%s District)' % (district.name, district.type_str))

                # Generate the district data set
                avg_year, unique = self.__generate_district_data(state, district, rs_by_year, assessments)

                # Print completion of district
                print('District created with average of %i students/year and %i total unique' % (avg_year, unique))
                student_avg_count += avg_year
                student_unique_count += unique

        # Print completion of state
        print('State %s created with average of %i students/year and %i total unique' % (state.name, student_avg_count, student_unique_count))

    def __generate_iabs(self):
        """
        generate iab assessment objects
        :return: generate assessments
        """
        assessments = {}

        # set up a progress bar
        progress_max = 0
        for subject, grade in itertools.product(sbac_in_config.SUBJECTS, GRADES_OF_CONCERN):
            progress_max += len(ASMT_YEARS) * len(sbac_in_config.IAB_NAMES[subject][grade]) * len(sbac_in_config.IAB_EFFECTIVE_DATES)
        bar = pyprind.ProgBar(progress_max, stream=sys.stdout, title='Generating IAB assessments')

        # generate iabs
        for subject, grade in itertools.product(sbac_in_config.SUBJECTS, GRADES_OF_CONCERN):
            for year, block, offset_date in itertools.product(ASMT_YEARS,
                                                              sbac_in_config.IAB_NAMES[subject][grade],
                                                              sbac_in_config.IAB_EFFECTIVE_DATES, ):
                date = datetime.date(year + offset_date.year - 2, offset_date.month, offset_date.day)
                key = sbac_interim_asmt_gen.get_iab_key(date, grade, subject, block)

                assessments[key] = sbac_interim_asmt_gen.generate_interim_assessment(date, year, subject, block, grade, self.id_gen,
                                                                                     generate_item_level=self.generate_item_level)
                # Output to requested mediums
                for worker in self.workers:
                    worker.write_iab(assessments[key])
                bar.update()

        return assessments

    def __generate_assessments(self):
        """
        generate summative and ica assessment objects
        :return: generate assessments
        """
        assessments = {}

        # set up a progress bar
        progress_max = len(ASMT_YEARS) * len(sbac_in_config.SUBJECTS) * len(GRADES_OF_CONCERN)
        bar = pyprind.ProgBar(progress_max, stream=sys.stdout, title='Generating Summative and ICA Assessments')

        for year in ASMT_YEARS:
            for subject in sbac_in_config.SUBJECTS:
                for grade in GRADES_OF_CONCERN:
                    # Create the summative assessment
                    asmt_key_summ = str(year) + 'summative' + str(grade) + subject
                    assessments[asmt_key_summ] = self.__create_and_write_assessment('SUMMATIVE', 'Spring', year, subject)

                    # Create the interim assessments
                    for period in INTERIM_ASMT_PERIODS:
                        asmt_key_intrm = str(year) + 'interim' + period + str(grade) + subject
                        asmt_intrm = self.__create_and_write_assessment('INTERIM COMPREHENSIVE', period, year, subject)
                        assessments[asmt_key_intrm] = asmt_intrm
                    bar.update()
        return assessments

    def __create_and_write_assessment(self, asmt_type, period, year, subject):
        """
        Create a new assessment object and write it out

        @param asmt_type: Type of assessment to create
        @param period: Period (month) of assessment to create
        @param year: Year of assessment to create
        @param subject: Subject of assessment to create
        @returns: New assessment object
        """
        # Create assessment
        asmt = sbac_asmt_gen.generate_assessment(asmt_type, period, year, subject, self.id_gen, generate_item_level=self.generate_item_level)

        for worker in self.workers:
            worker.write_assessment(asmt)
        return asmt

    def __build_registration_system(self, years=YEARS):
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
        rs = sbac_hier_gen.generate_registration_system(start_year, str(start_year - 1) + '-02-25', self.id_gen)

        # Update it over every year
        for year in YEARS:
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
                school = sbac_hier_gen.generate_school(school_type, district, self.id_gen)
                ih = sbac_hier_gen.generate_institution_hierarchy(state, district, school, self.id_gen)
                hierarchies.append(ih)
                inst_hiers[school.guid] = ih
                schools.append(school)

        # Write out hierarchies for this district
        for worker in self.workers:
            worker.write_hierarchies(hierarchies)

        # Some explicit garbage collection
        del hierarchies

    def __generate_district_data(self, state: State, district: District, reg_sys_by_year: {str: RegistrationSystem}, assessments: {str: InterimAssessment}):
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
        schools_by_grade = sbac_hier_gen.sort_schools_by_grade(schools)

        pop_schools_with_groupings = {}
        # Student grouping is enabled for district using Student_grouping_rate
        if district.student_grouping:
            schools_with_groupings = sbac_hier_gen.set_up_schools_with_groupings(schools, GRADES_OF_CONCERN)
            pop_schools_with_groupings = sbac_hier_gen.populate_schools_with_groupings(schools_with_groupings, self.id_gen)

        # Begin processing the years for data
        unique_students = {}
        students = {}
        student_count = 0

        # calculate the progress bar max and start the progress
        progress_max = len(sbac_hier_gen.set_up_schools_with_grades(schools, GRADES_OF_CONCERN)) * len(YEARS)
        bar = pyprind.ProgBar(progress_max, stream=sys.stdout, title='Generating assessments outcome for schools')

        for asmt_year in YEARS:
            # Prepare output file names
            reg_system = reg_sys_by_year[asmt_year]

            # Set up a dictionary of schools and their grades
            schools_with_grades = sbac_hier_gen.set_up_schools_with_grades(schools, GRADES_OF_CONCERN)

            # Advance the students forward in the grades
            for guid, student in students.items():
                # Assign the registration system and bump up the record ID
                student.reg_sys = reg_system
                student.rec_id_sr = self.id_gen.get_rec_id('sr_student')

                # Move the student forward (false from the advance method means the student disappears)
                if sbac_pop_gen.advance_student(student, schools_by_grade):
                    schools_with_grades[student.school][student.grade].append(student)

            # With the students moved around, we will re-populate empty grades and create assessments with outcomes for
            # the students
            for school, grades in schools_with_grades.items():
                # Process the whole school
                student_count += self.__process_school(grades, school, students, unique_students, state, district,
                                                       reg_system, asmt_year, inst_hiers[school.guid], assessments,
                                                       pop_schools_with_groupings)
                bar.update()

        unique_student_count = len(unique_students)

        # Some explicit garbage collection
        del inst_hiers
        del schools
        del schools_by_grade
        del students
        del unique_students

        # Return the average student count
        return int(student_count // len(ASMT_YEARS)), unique_student_count

    def __process_school(self, grades, school, students, unique_students, state, district, reg_system: RegistrationSystem,
                         asmt_year, inst_hier, assessments, pop_schools_with_groupings):

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
            sbac_pop_gen.repopulate_school_grade(school, grade, grade_students, self.id_gen, state, reg_system, asmt_year)
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
                        sbac_asmt_gen.create_assessment_outcome_objects(student, asmt_summ, interim_asmts, inst_hier, self.id_gen,
                                                                        assessment_results, skip_rate,
                                                                        generate_item_level=self.generate_item_level)

                        if not student.skip_iab:
                            sbac_interim_asmt_gen.create_iab_outcome_objects(student,
                                                                             asmt_year,
                                                                             grade,
                                                                             subject,
                                                                             assessments,
                                                                             inst_hier,
                                                                             self.id_gen,
                                                                             iab_results,
                                                                             generate_item_level=self.generate_item_level)

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
        self.__write_school_data(asmt_year, reg_system.guid_sr, dim_students, sr_students, assessment_results, iab_results,
                                 state.code, district.guid)
        del dim_students
        del sr_students
        del assessment_results
        del iab_results

        return student_count

    def __write_school_data(self, asmt_year, rs_guid, dim_students, sr_students, assessment_results, iab_results, state_code, district_id):
        """
        Write student and assessment data for a school to one or more output formats.

        @param asmt_year: Current academic year
        @param dim_students: Students to write to dim_student star-schema CSVs/postgres tables
        @param sr_students: Students to write to registration landing zone/star-schema CSV/postgres table
        @param assessment_results: Assessment outcomes to write to landing zone/star-schema CSV/postgres table
        @param iab_results: IAB assessment outcomes
        @param state_code: state code
        @param district_id: district it
        """

        for worker in self.workers:
            worker.write_students_dim(dim_students)
            worker.write_students_reg(sr_students, rs_guid, asmt_year)

        # Write assessment results if we have them; also optionally to landing zone CSV, star-schema CSV, and/or to postgres
        if asmt_year in ASMT_YEARS:
            for guid, iab_result in iab_results.items():
                for worker in self.workers:
                    worker.write_iab_outcome(iab_result, guid)

            for guid, results in assessment_results.items():
                # todo: this needs to be refactored
                if self.generate_item_level:
                    for sao in results:
                        self.__write_item_level_date(sao, state_code, district_id)

                for worker in self.workers:
                    worker.write_assessment_outcome(results, guid)

    def __write_item_level_date(self, sao: AssessmentOutcome, state_code, district_id):
        try:
            asmt = sao.assessment
            # Only write out summative item level results
            if asmt.asmt_type == 'SUMMATIVE':
                it_dir_path = os.path.join(state_code, str(asmt.period_year), asmt.asmt_type, DG_FILTERS['date_Ymd'](asmt.effective_date), asmt.subject,
                                           str(sao.student.grade), district_id)
                it_file_path = os.path.join(it_dir_path, sbac_out_config.LZ_ITEMDATA_FORMAT['name'].replace('<STUDENT_ID>', sao.student.guid_sr))

                if not os.path.exists(os.path.join(self.out_path_root, it_dir_path)):
                    os.makedirs(os.path.join(self.out_path_root, it_dir_path))

                csv_writer.write_records_to_file(it_file_path, sbac_out_config.LZ_ITEMDATA_FORMAT['columns'], sao.item_level_data, root_path=self.out_path_root)

        finally:
            pass
