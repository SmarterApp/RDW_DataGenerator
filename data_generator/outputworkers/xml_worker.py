from xml.etree.ElementTree import Element, SubElement, tostring

from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.interimassessmentoutcome import InterimAssessmentOutcome
from data_generator.outputworkers.worker import Worker


class XmlWorker(Worker):
    def __init__(self, out_path_root):
        self.out_path_root = out_path_root

    def prepare(self):
        # TODO - clean out_path_root
        pass

    def cleanup(self):
        pass

    def write_iab_outcome(self, results: [InterimAssessmentOutcome], assessment_guid):
        self.write_asmt_to_file(results[0])

    def write_assessment_outcome(self, results: [AssessmentOutcome], assessment_guid, state_code, district_id):
        self.write_asmt_to_file(results[0])

    # TODO - more elegant approach to mapping model to XML
    def write_asmt_to_file(self, outcome: AssessmentOutcome):
        root = Element('TDSReport')

        # write Test
        asmt = outcome.assessment
        test = SubElement(root, 'Test')
        test.set('testId', asmt.id)
        test.set('name', asmt.name)
        test.set('bankKey', asmt.bank_key)
        test.set('subject', asmt.subject)
        test.set('grade', '{:02}'.format(asmt.grade))
        test.set('assessmentType', self.map_asmt_type(asmt.type))
        test.set('academicYear', str(asmt.year))
        test.set('assessmentVersion', asmt.version)
        test.set('contract', asmt.contract)
        test.set('mode', asmt.mode)

        # write Examinee
        student = outcome.student
        examinee = SubElement(root, 'Examinee')
        examinee.set('key', str(student.rec_id))

        # TODO - work out SSID and AlternateSSID
        self.add_examinee_attribute(examinee, 'SSID', student.external_ssid)
        self.add_examinee_attribute(examinee, 'Birthdate', student.dob)
        self.add_examinee_attribute(examinee, 'FirstName', student.first_name)
        self.add_examinee_attribute(examinee, 'MiddleName', student.middle_name)
        self.add_examinee_attribute(examinee, 'LastOrSurname', student.last_name)
        self.add_examinee_attribute(examinee, 'Sex', self.map_gender(student.gender))
        self.add_examinee_attribute(examinee, 'GradeLevelWhenAssessed', '{:02}'.format(student.grade))
        self.add_examinee_attribute(examinee, 'HispanicOrLatinoEthnicity', self.map_yes_no(student.eth_hispanic))
        self.add_examinee_attribute(examinee, 'AmericanIndianOrAlaskaNative', self.map_yes_no(student.eth_amer_ind))
        self.add_examinee_attribute(examinee, 'Asian', self.map_yes_no(student.eth_asian))
        self.add_examinee_attribute(examinee, 'BlackOrAfricanAmerican', self.map_yes_no(student.eth_black))
        self.add_examinee_attribute(examinee, 'White', self.map_yes_no(student.eth_white))
        self.add_examinee_attribute(examinee, 'NativeHawaiianOrOtherPacificIslander', self.map_yes_no(student.eth_pacific))
        self.add_examinee_attribute(examinee, 'TwoOrMoreRaces', self.map_yes_no(student.eth_multi))
        # self.add_examinee_attribute(examinee, 'IDEAIndicator', self.map_yes_no(student.))
        self.add_examinee_attribute(examinee, 'LEPStatus', self.map_yes_no(student.prg_lep))
        self.add_examinee_attribute(examinee, 'Section504Status', self.map_yes_no(student.prg_sec504))
        self.add_examinee_attribute(examinee, 'EconomicDisadvantageStatus', self.map_yes_no(student.prg_econ_disad))
        self.add_examinee_attribute(examinee, 'LanguageCode', student.lang_code)
        self.add_examinee_attribute(examinee, 'EnglishLanguageProficiencyLevel', student.lang_prof_level)
        # TODO - there are a few more of these

        hierarchy = outcome.inst_hierarchy
        self.add_examinee_relationship(examinee, 'StateAbbreviation', hierarchy.state.code)
        self.add_examinee_relationship(examinee, 'StateName', hierarchy.state.name)
        self.add_examinee_relationship(examinee, 'DistrictID', hierarchy.district.guid)
        self.add_examinee_relationship(examinee, 'DistrictName', hierarchy.district.name)
        self.add_examinee_relationship(examinee, 'SchoolID', hierarchy.school.guid)
        self.add_examinee_relationship(examinee, 'SchoolName', hierarchy.school.name)

        # write Opportunity
        #   TODO - write Accomodations
        #   TODO - write Segments
        #   TODO - write Items
        opportunity = SubElement(root, 'Opportunity')
        opportunity.set('server', outcome.server)
        opportunity.set('datbase', outcome.database)
        opportunity.set('clientName', outcome.client_name)
        opportunity.set('status', outcome.status)
        opportunity.set('completeness', outcome.completeness)

        print(tostring(root, 'unicode'))

    def add_examinee_attribute(self, parent, name, value):
        if value:
            attr = SubElement(parent, 'ExamineeAttribute')
            attr.set('context', 'FINAL')
            attr.set('name', name)
            attr.set('value', str(value))
            # TODO - attr.set('contextDate', )

    def add_examinee_relationship(self, parent, name, value):
        if value:
            attr = SubElement(parent, 'ExamineeRelationship')
            attr.set('context', 'FINAL')
            attr.set('name', name)
            attr.set('value', str(value))
            # TODO - attr.set('contextDate', )

    def map_asmt_type(self, value):
        # TODO - map various possibilities to expected values
        # TODO - map assessmentType from 'INTERIM ASSESSMENT BLOCKS' to 'IAB' or whatever
        if 'summative' in value.lower(): return 'SUM'
        if 'block' in value.lower(): return 'IAB'
        return 'ICA'

    def map_gender(self, value):
        if 'female' == value.lower(): return 'Female'
        if 'male' == value.lower(): return 'Male'
        return None

    def map_yes_no(self, value):
        return 'Yes' if value else 'No'
