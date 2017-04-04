from xml.etree.ElementTree import Element, SubElement, tostring

from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.interimassessmentoutcome import InterimAssessmentOutcome
from data_generator.outputworkers.worker import Worker


class XmlWorker(Worker):
    def __init__(self, out_path_root):
        self.out_path_root = out_path_root

    def prepare(self):
        # TODO - clean out_path_root?
        pass

    def cleanup(self):
        pass

    def write_iab_outcome(self, results: [InterimAssessmentOutcome], assessment_guid):
        self.write_asmt_to_file(results[0])

    def write_assessment_outcome(self, results: [AssessmentOutcome], assessment_guid, state_code, district_id):
        self.write_asmt_to_file(results[0])

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
        self.add_examinee_attribute(examinee, 'SSID', student.external_ssid, outcome.date_taken)
        self.add_examinee_attribute(examinee, 'Birthdate', student.dob, outcome.date_taken)
        self.add_examinee_attribute(examinee, 'FirstName', student.first_name, outcome.date_taken)
        self.add_examinee_attribute(examinee, 'MiddleName', student.middle_name, outcome.date_taken)
        self.add_examinee_attribute(examinee, 'LastOrSurname', student.last_name, outcome.date_taken)
        self.add_examinee_attribute(examinee, 'Sex', self.map_gender(student.gender), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'GradeLevelWhenAssessed', '{:02}'.format(student.grade), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'HispanicOrLatinoEthnicity', self.map_yes_no(student.eth_hispanic), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'AmericanIndianOrAlaskaNative', self.map_yes_no(student.eth_amer_ind), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'Asian', self.map_yes_no(student.eth_asian), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'BlackOrAfricanAmerican', self.map_yes_no(student.eth_black), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'White', self.map_yes_no(student.eth_white), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'NativeHawaiianOrOtherPacificIslander', self.map_yes_no(student.eth_pacific), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'TwoOrMoreRaces', self.map_yes_no(student.eth_multi), outcome.date_taken)
        # self.add_examinee_attribute(examinee, 'IDEAIndicator', self.map_yes_no(student.), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'LEPStatus', self.map_yes_no(student.prg_lep), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'Section504Status', self.map_yes_no(student.prg_sec504), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'EconomicDisadvantageStatus', self.map_yes_no(student.prg_econ_disad), outcome.date_taken)
        self.add_examinee_attribute(examinee, 'LanguageCode', student.lang_code, outcome.date_taken)
        self.add_examinee_attribute(examinee, 'EnglishLanguageProficiencyLevel', student.lang_prof_level, outcome.date_taken)
        # TODO - there are a few more of these

        hierarchy = outcome.inst_hierarchy
        self.add_examinee_relationship(examinee, 'StateAbbreviation', hierarchy.state.code, outcome.date_taken)
        self.add_examinee_relationship(examinee, 'StateName', hierarchy.state.name, outcome.date_taken)
        self.add_examinee_relationship(examinee, 'DistrictID', hierarchy.district.guid, outcome.date_taken)
        self.add_examinee_relationship(examinee, 'DistrictName', hierarchy.district.name, outcome.date_taken)
        self.add_examinee_relationship(examinee, 'SchoolID', hierarchy.school.guid, outcome.date_taken)
        self.add_examinee_relationship(examinee, 'SchoolName', hierarchy.school.name, outcome.date_taken)

        # write Opportunity
        opportunity = SubElement(root, 'Opportunity')
        opportunity.set('server', outcome.server)
        opportunity.set('datbase', outcome.database)
        opportunity.set('clientName', outcome.client_name)
        opportunity.set('status', outcome.status)
        opportunity.set('completeness', outcome.completeness)
        opportunity.set('key', outcome.guid)
        opportunity.set('oppId', str(outcome.rec_id))
        opportunity.set('opportunity', '5')         # TODO
        opportunity.set('startDate', str(outcome.start_date))
        opportunity.set('statusDate', str(outcome.status_date))
        opportunity.set('dateCompleted', str(outcome.submit_date))
        opportunity.set('itemCount', str(len(outcome.item_data)))
        opportunity.set('ftCount', '0')
        opportunity.set('pauseCount', '0')
        opportunity.set('abnormalStarts', '0')
        opportunity.set('gracePeriodRestarts', '0')
        # opportunity.set('taId', None)
        # opportunity.set('taName', None)
        # opportunity.set('sessionId', None)
        opportunity.set('windowId', 'WINDOW_ID')    # TODO
        # opportunity.set('windowOpportunity', None)
        opportunity.set('administrationCondition', 'Valid')
        opportunity.set('assessmentParticipantSessionPlatformUserAgent', '')
        opportunity.set('effectiveDate', str(asmt.effective_date))

        segment = SubElement(opportunity, 'Segment')
        segment.set('id', outcome.assessment.segment.id)
        segment.set('position', str(outcome.assessment.segment.position))
        segment.set('algorithm', outcome.assessment.segment.algorithm)
        segment.set('algorithmVersion', outcome.assessment.segment.algorithm_version)

        # TODO - Accommodations

        # TODO - Score

        for item_data in outcome.item_data:
            item = SubElement(opportunity, 'Item')
            item.set('bankKey', item_data.item.bank_key)
            item.set('key', item_data.item.item_key)
            item.set('position', str(item_data.item.position))
            item.set('segmentId', item_data.item.segment_id)
            item.set('format', item_data.item.type)
            item.set('operational', item_data.item.operational)
            item.set('isSelected', item_data.item.is_selected)
            item.set('adminDate', str(item_data.admin_date))
            item.set('numberVisits', str(item_data.number_visits))
            item.set('pageNumber', str(item_data.page_number))
            item.set('pageVisits', str(item_data.page_visits))
            item.set('pageTime', str(item_data.page_time))
            item.set('responseDuration', str(item_data.page_time / 1000.0))
            item.set('dropped', item_data.dropped)
            response = SubElement(item, 'Response')
            response.set('date', str(item_data.response_date))
            response.set('type', 'value')
            response.text = item_data.response_value

        # TODO - write to file; filename will be outcome id?
        print(tostring(root, 'unicode'))

    def add_examinee_attribute(self, parent, name, value, contextDate):
        if value:
            attr = SubElement(parent, 'ExamineeAttribute')
            attr.set('context', 'FINAL')
            attr.set('name', name)
            attr.set('value', str(value))
            attr.set('contextDate', str(contextDate))

    def add_examinee_relationship(self, parent, name, value, contextDate):
        if value:
            attr = SubElement(parent, 'ExamineeRelationship')
            attr.set('context', 'FINAL')
            attr.set('name', name)
            attr.set('value', str(value))
            attr.set('contextDate', str(contextDate))

    def map_asmt_type(self, value):
        if 'summative' in value.lower(): return 'SUM'
        if 'block' in value.lower(): return 'IAB'
        return 'ICA'

    def map_gender(self, value):
        if 'female' == value.lower(): return 'Female'
        if 'male' == value.lower(): return 'Male'
        return None

    def map_yes_no(self, value):
        return 'Yes' if value else 'No'
