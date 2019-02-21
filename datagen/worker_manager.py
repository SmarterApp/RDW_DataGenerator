import copy
import datetime
import itertools
import random
import sys

import pyprind

import datagen.config.cfg as cfg
import datagen.generators.hierarchy as hier_gen
import datagen.generators.iab_assessment as iab_asmt_gen
import datagen.generators.population as pop_gen
import datagen.generators.summative_or_ica_assessment as asmt_gen
import datagen.util.hierarchy as hier_util
from datagen.model.assessment import Assessment
from datagen.model.district import District
from datagen.model.registrationsystem import RegistrationSystem
from datagen.model.school import School
from datagen.model.state import State
from datagen.outputworkers.worker import Worker
from datagen.outputworkers.xml_worker import XmlWorker
from datagen.readers.tabulator_reader import load_assessments
from datagen.util.id_gen import IDGen

# constants used when generating assessment packages
ASMT_YEARS = [2017, 2018, 2019]  # Expected sorted lowest to highest

# These are global regardless of team
GRADES_OF_CONCERN = {3, 4, 5, 6, 7, 8, 11}  # Made as a set for intersection later


class WorkerManager(Worker):
    def __init__(self, args):
        self._args = args

        # Save output directory
        self.out_path_root = args.out_dir
        self.state_cfg = {'name': args.state_name, 'code': args.state_code, 'type': args.state_type}
        self.hier_source = args.hier_source

        # Set up output
        self.workers = []
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

        self.id_gen = IDGen()

    def cleanup(self):
        for worker in self.workers:
            worker.cleanup()

    def prepare(self):
        for worker in self.workers:
            worker.prepare()

    def run(self):
        state, districts, schools = self.__hierarchy()

        assessments = self.__assessment_packages()
        if len(assessments) == 0:
            print('No assessment packages found')
            return

        # Process the state
        self.__generate_state_data(state, districts, schools, assessments)

    def __hierarchy(self):
        """
        Generate or load the hierarchy of state, districts, schools

        :return:
        """
        if self.hier_source == 'generate':
            state, districts, schools = hier_util.generate_hierarchy(self.state_cfg['type'], self.state_cfg['name'], self.state_cfg['code'], self.id_gen)
        else:
            state, districts, schools = hier_util.read_hierarchy(self.hier_source)

        # call hook for workers to write hierarchies
        hierarchies = [hier_gen.generate_institution_hierarchy(school.district.state, school.district, school, self.id_gen) for school in schools]
        for worker in self.workers:
            worker.write_hierarchies(hierarchies)
        del hierarchies

        return state, districts, schools

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

    def __subjects(self, assessments: [Assessment]):
        """
        Return the sorted list of subjects represented by assessment packages.
        :param assessments: assessments
        :return: sorted list of subjects, e.g. ['ELA', 'Math']
        """
        return sorted(set(map(lambda asmt: asmt.subject, assessments)))

    def __generate_state_data(self, state: State, districts: [District], schools: [School], assessments: [Assessment]):
        """
        Generate an entire data set for a single state.

        @param state: State to generate data for
        """
        print('Creating results for state: %s' % state.name)

        # build registration system by years
        rs_by_year = self.__build_registration_system(self.__years(assessments))

        # Build the districts
        student_avg_count = 0
        student_unique_count = 0
        for district in districts:
            print('\nCreating results for district %s (%s District)' % (district.name, district.type_str))

            # collect schools for the district
            district_schools = [s for s in schools if s.district == district]

            # Generate the district data set
            avg_year, unique = self.__generate_district_data(district_schools, rs_by_year, assessments)

            # Print completion of district
            print('District results created with average of %i students/year and %i total unique' % (avg_year, unique))
            student_avg_count += avg_year
            student_unique_count += unique

        # Print completion of state
        print('State results created with average of %i students/year and %i total unique' % (student_avg_count, student_unique_count))

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
                assessments.append(self.__create_and_write_assessment('SUMMATIVE', year, subject, grade))
            if self.ica_pkg:
                assessments.append(self.__create_and_write_assessment('INTERIM COMPREHENSIVE', year, subject, grade))
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

    def __create_and_write_assessment(self, type, year, subject, grade):
        asmt = asmt_gen.generate_assessment(type, year, subject, grade, self.id_gen, gen_item=self.gen_item)
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

    def __generate_district_data(self, schools: [School], reg_sys_by_year: {str: RegistrationSystem}, assessments: [Assessment]):
        """
        Generate an entire data set for all schools in a single district.

        @param schools: schools for the district
        @param assessments: Dictionary of all assessment objects
        """
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
                student_count += self.__process_school(grades, school, students, unique_students, reg_system, year, assessments)
                bar.update()

        unique_student_count = len(unique_students)

        # Some explicit garbage collection
        del schools_by_grade
        del students
        del unique_students

        # Return the average student count
        return int(student_count // len(years)), unique_student_count

    def __process_school(self, grades, school, students, unique_students, reg_system: RegistrationSystem, year, assessments):

        district = school.district
        state = district.state

        # get all subjects represented by assessment packages
        subjects = self.__subjects(assessments)

        # Grab the assessment rates by subjects
        asmt_skip_rates_by_subject = state.config['subject_skip_percentages']
        # hack for custom subjects
        for subject in subjects:
            if subject not in asmt_skip_rates_by_subject:
                asmt_skip_rates_by_subject[subject] = asmt_skip_rates_by_subject['Math']

        # Process the whole school
        assessment_results = {}
        iab_results = {}
        sr_students = []
        dim_students = []
        student_count = 0

        for grade, grade_students in grades.items():
            # Potentially re-populate the student population
            pop_gen.repopulate_school_grade(school, grade, grade_students, self.id_gen, reg_system, year, subjects)
            student_count += len(grade_students)

            pop_gen.assign_student_groups(school, grade, grade_students, self.id_gen, subjects)

            # collect any assessments for this year and grade
            asmts = list(filter(lambda asmt: asmt.year == year and asmt.grade == grade, assessments))
            for asmt in asmts:
                date_taken = self.__date_taken_for_asmt(asmt)
                for student in grade_students:
                    if asmt.is_iab():
                        if school.takes_interim_asmts and random.random() < cfg.IAB_STUDENT_RATE:
                            iab_asmt_gen.create_iab_outcome_object(date_taken, student, asmt, self.id_gen,
                                iab_results, gen_item=self.gen_item)
                    else:
                        asmt_gen.create_assessment_outcome_object(date_taken, student, asmt, self.id_gen,
                            assessment_results, asmt_skip_rates_by_subject[asmt.subject], gen_item=self.gen_item)

                    # Make sure we have the student for the next run and for metrics
                    # (bit repetitive to do it in the inner loop but probably okay for now)
                    if student.guid not in students:
                        students[student.guid] = student
                        dim_students.append(student)
                    if student.guid not in unique_students:
                        unique_students[student.guid] = True

            # collect all the students for registration output (randomly missing a few)
            sr_students.extend([s for s in grade_students if random.random() < cfg.HAS_ASMT_RESULT_IN_SR_FILE_RATE])

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
        @param dim_students: Students to write
        @param sr_students: Students to write
        @param assessment_results: Assessment outcomes to write
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

    def __date_taken_for_asmt(self, asmt: Assessment):
        """
        Generates a random date for an assessment.
        IABs can be pretty much any time from mid-Sep to mid-March
        ICAs will be late-January
        Summatives will be early May

        :param asmt: assessment
        :return: date taken
        """
        if asmt.is_iab():
            date_taken = datetime.date(asmt.year-1, 9, 15) + datetime.timedelta(days=random.randint(0, 180))
        elif asmt.is_summative():
            date_taken = datetime.date(asmt.year, 5, 10)
        else:
            date_taken = datetime.date(asmt.year, 1, 21)
        return self.__weekday_near(date_taken)

    def __weekday_near(self, value: datetime.date):
        """
        Generates a random date that is near the given target date and is a weekday.
        For now this is simple: shift date randomly +-3, then make sure it's not a weekend.

        :param value: date to be near
        :return: new date
        """
        value += datetime.timedelta(days=random.randint(-3, 3))
        if value.weekday() == 5: value += datetime.timedelta(days=-1)     # Sat -> Fri
        elif value.weekday() == 6: value += datetime.timedelta(days=+1)   # Sun -> Mon
        return value
