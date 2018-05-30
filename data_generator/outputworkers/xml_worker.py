import json
from collections import OrderedDict
from xml.etree.ElementTree import Element, SubElement, tostring

import os

from data_generator.model.assessment import Assessment
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.institutionhierarchy import InstitutionHierarchy
from data_generator.outputworkers.worker import Worker
from data_generator.writers import tabulator_writer

CLAIM_MEASURES = {
    'Math': ['1', 'SOCK_2', '3', ''],
    'ELA': ['SOCK_R', '2-W', 'SOCK_LS', '4-CR']
}


class XmlWorker(Worker):
    def __init__(self, out_path_root):
        self.out_path_root = out_path_root

    def prepare(self):
        pass

    def cleanup(self):
        pass

    def write_hierarchies(self, hierarchies: [InstitutionHierarchy]):
        districts = {}
        schools = {}

        # because each district is generated individually, we need to read the file to
        # get previous districts, merge the new ones, then rewrite the file ...
        file = os.path.join(self.out_path_root, 'organizations.json')
        if os.path.isfile(file):
            with open(file, "r") as f:
                org = json.load(f)
                if 'districts' in org: districts = {d['entityId']: d for d in org['districts']}
                if 'institutions' in org: schools = {s['entityId']: s for s in org['institutions']}

        for hierarchy in hierarchies:
            if hierarchy.district.id not in districts:
                districts[hierarchy.district.id] = {
                    'entityId': hierarchy.district.id,
                    'entityName': hierarchy.district.name,
                    'entityType': 'DISTRICT',
                    'parentEntityType': 'STATE',
                    'parentEntityId': hierarchy.state.code
                }
            if hierarchy.school.id not in schools:
                schools[hierarchy.school.id] = {
                    'entityId': hierarchy.school.id,
                    'entityName': hierarchy.school.name,
                    'entityType': 'INSTITUTION',
                    'parentEntityType': 'DISTRICT',
                    'parentEntityId': hierarchy.district.id
                }

        with open(file, "w") as f:
            # force output order to be same as org hierarchy
            json.dump(OrderedDict([('districts', list(districts.values())), ('institutions', list(schools.values()))]), f, indent=2)

    def write_assessments(self, asmts: [Assessment]):
        tabulator_writer.write_assessments(os.path.join(self.out_path_root, 'assessments.csv'), asmts, )

    def write_iab_outcome(self, results: [AssessmentOutcome], assessment_guid):
        for result in results:
            self.write_asmt_to_file(result)

    def write_assessment_outcome(self, results: [AssessmentOutcome], assessment_guid, state_code, district_id):
        for result in results:
            self.write_asmt_to_file(result)

    def write_asmt_to_file(self, outcome: AssessmentOutcome):
        # skip inactive or deleted outcomes
        if outcome.result_status != 'C':
            return

        root = Element('TDSReport')

        # write Test
        asmt = outcome.assessment
        test = SubElement(root, 'Test')
        # in TRT, the testId is the name and the name is the id
        test.set('testId', asmt.name)
        test.set('name', asmt.id)
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

        contextDateStr = outcome.status_date.isoformat()
        self.add_examinee_attribute(examinee, 'StudentIdentifier', student.id, contextDateStr)
        self.add_examinee_attribute(examinee, 'AlternateSSID', student.external_ssid, contextDateStr)
        self.add_examinee_attribute(examinee, 'Birthdate', student.dob, contextDateStr)
        self.add_examinee_attribute(examinee, 'FirstName', student.first_name, contextDateStr)
        self.add_examinee_attribute(examinee, 'MiddleName', student.middle_name, contextDateStr)
        self.add_examinee_attribute(examinee, 'LastOrSurname', student.last_name, contextDateStr)
        self.add_examinee_attribute(examinee, 'Sex', self.map_gender(student.gender), contextDateStr)
        self.add_examinee_attribute(examinee, 'GradeLevelWhenAssessed', '{:02}'.format(student.grade), contextDateStr)
        self.add_examinee_attribute(examinee, 'HispanicOrLatinoEthnicity', self.map_yes_no(student.eth_hispanic), contextDateStr)
        self.add_examinee_attribute(examinee, 'AmericanIndianOrAlaskaNative', self.map_yes_no(student.eth_amer_ind), contextDateStr)
        self.add_examinee_attribute(examinee, 'Asian', self.map_yes_no(student.eth_asian), contextDateStr)
        self.add_examinee_attribute(examinee, 'Filipino', self.map_yes_no(student.eth_filipino), contextDateStr)
        self.add_examinee_attribute(examinee, 'BlackOrAfricanAmerican', self.map_yes_no(student.eth_black), contextDateStr)
        self.add_examinee_attribute(examinee, 'White', self.map_yes_no(student.eth_white), contextDateStr)
        self.add_examinee_attribute(examinee, 'NativeHawaiianOrOtherPacificIslander', self.map_yes_no(student.eth_pacific), contextDateStr)
        self.add_examinee_attribute(examinee, 'DemographicRaceTwoOrMoreRaces', self.map_yes_no(student.eth_multi), contextDateStr)
        self.add_examinee_attribute(examinee, 'IDEAIndicator', self.map_yes_no(student.prg_iep), contextDateStr)
        self.add_examinee_attribute(examinee, 'LEPStatus', self.map_yes_no(student.prg_lep), contextDateStr)
        self.add_examinee_attribute(examinee, 'LimitedEnglishProficiencyEntryDate', student.prg_lep_entry_date, contextDateStr)
        self.add_examinee_attribute(examinee, 'LEPExitDate', student.prg_lep_exit_date, contextDateStr)
        self.add_examinee_attribute(examinee, 'Section504Status', self.map_yes_no(student.prg_sec504), contextDateStr)
        self.add_examinee_attribute(examinee, 'EconomicDisadvantageStatus', self.map_yes_no(student.prg_econ_disad), contextDateStr)
        self.add_examinee_attribute(examinee, 'LanguageCode', student.lang_code, contextDateStr)
        self.add_examinee_attribute(examinee, 'EnglishLanguageProficiencyLevel', student.lang_prof_level, contextDateStr)
        self.add_examinee_attribute(examinee, 'EnglishLanguageAcquisitionStatus', student.elas, contextDateStr)
        self.add_examinee_attribute(examinee, 'EnglishLanguageAcquisitionStatusStartDate', student.elas_start_date, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_1_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_2_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_3_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_4_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_5_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_6_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_7_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_8_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_9_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'StudentGroupName', student.group_10_text, contextDateStr)
        self.add_examinee_attribute(examinee, 'Advancement', self.map_advancement(student), contextDateStr)
        self.add_examinee_attribute(examinee, 'Capability', student.capability.get(asmt.subject, 0.0), contextDateStr)

        hierarchy = outcome.inst_hierarchy
        self.add_examinee_relationship(examinee, 'StateAbbreviation', hierarchy.state.code, contextDateStr)
        self.add_examinee_relationship(examinee, 'StateName', hierarchy.state.name, contextDateStr)
        self.add_examinee_relationship(examinee, 'DistrictId', hierarchy.district.id, contextDateStr)
        self.add_examinee_relationship(examinee, 'DistrictName', hierarchy.district.name, contextDateStr)
        self.add_examinee_relationship(examinee, 'SchoolId', hierarchy.school.id, contextDateStr)
        self.add_examinee_relationship(examinee, 'SchoolName', hierarchy.school.name, contextDateStr)

        # write Opportunity
        opportunity = SubElement(root, 'Opportunity')
        opportunity.set('server', outcome.server)
        opportunity.set('database', outcome.database)
        opportunity.set('clientName', outcome.client_name)
        opportunity.set('status', outcome.status)
        opportunity.set('completeness', outcome.completeness)
        opportunity.set('completeStatus', outcome.completeness)
        opportunity.set('key', str(outcome.rec_id))
        opportunity.set('oppId', str(outcome.rec_id))
        opportunity.set('opportunity', '5')
        opportunity.set('startDate', outcome.start_date.isoformat())
        opportunity.set('statusDate', outcome.status_date.isoformat())
        opportunity.set('dateCompleted', outcome.submit_date.isoformat())
        opportunity.set('itemCount', str(len(outcome.item_data)))
        opportunity.set('ftCount', '0')
        opportunity.set('pauseCount', '0')
        opportunity.set('abnormalStarts', '0')
        opportunity.set('gracePeriodRestarts', '0')
        # opportunity.set('taId', None)
        # opportunity.set('taName', None)
        opportunity.set('sessionId', outcome.session)
        opportunity.set('windowId', 'WINDOW_ID')
        # opportunity.set('windowOpportunity', None)
        opportunity.set('administrationCondition', outcome.admin_condition)
        opportunity.set('assessmentParticipantSessionPlatformUserAgent', '')
        opportunity.set('effectiveDate', asmt.effective_date.isoformat())

        if asmt.segment:
            segment = SubElement(opportunity, 'Segment')
            segment.set('id', asmt.segment.id)
            segment.set('position', str(asmt.segment.position))
            segment.set('algorithm', asmt.segment.algorithm)
            segment.set('algorithmVersion', asmt.segment.algorithm_version)

        for (type, code, value) in outcome.accommodations:
            accommodation = SubElement(opportunity, 'Accommodation')
            accommodation.set('type', type)
            accommodation.set('code', code)
            accommodation.set('value', value)

        self.add_scale_score(opportunity, 'Overall',
            outcome.overall_score, outcome.overall_score_range_min, outcome.overall_perf_lvl)
        if not asmt.is_iab():
            self.add_scale_score(opportunity, CLAIM_MEASURES[asmt.subject][0],
                outcome.claim_1_score, outcome.claim_1_score_range_min, outcome.claim_1_perf_lvl)
            self.add_scale_score(opportunity, CLAIM_MEASURES[asmt.subject][1],
                outcome.claim_2_score, outcome.claim_2_score_range_min, outcome.claim_2_perf_lvl)
            self.add_scale_score(opportunity, CLAIM_MEASURES[asmt.subject][2],
                outcome.claim_3_score, outcome.claim_3_score_range_min, outcome.claim_3_perf_lvl)
            self.add_scale_score(opportunity, CLAIM_MEASURES[asmt.subject][3],
                outcome.claim_4_score, outcome.claim_4_score_range_min, outcome.claim_4_perf_lvl)

        for item_data in outcome.item_data:
            item = SubElement(opportunity, 'Item')
            item.set('bankKey', item_data.item.bank_key)
            item.set('key', item_data.item.item_key)
            item.set('position', str(item_data.item.position))
            item.set('segmentId', item_data.item.segment_id)
            item.set('format', item_data.item.type)
            item.set('operational', item_data.item.operational)
            item.set('isSelected', item_data.is_selected)
            item.set('adminDate', item_data.admin_date.isoformat())
            item.set('numberVisits', str(item_data.number_visits))
            item.set('pageNumber', str(item_data.page_number))
            item.set('pageVisits', str(item_data.page_visits))
            item.set('pageTime', str(item_data.page_time))
            item.set('responseDuration', str(item_data.page_time / 1000.0))
            item.set('dropped', item_data.dropped)
            item.set('score', str(item_data.score))
            item.set('scoreStatus', item_data.score_status)
            item.set('mimeType', 'text/plain')      # TODO

            # summative results should not have item response included (business policy)
            if not asmt.is_summative():
                response = SubElement(item, 'Response')
                response.set('date', item_data.response_date.isoformat())
                response.set('type', 'value')
                response.text = item_data.response_value

            if item_data.sub_scores:
                scoreInfo = self.add_score_info(item, 'Overall', item_data.score)
                subScoreList = SubElement(scoreInfo, 'SubScoreList')
                self.add_score_info(subScoreList, 'Organization/Purpose', item_data.sub_scores[0])
                self.add_score_info(subScoreList, 'Evidence/Elaboration', item_data.sub_scores[1])
                self.add_score_info(subScoreList, 'Conventions', item_data.sub_scores[2])

        xml = tostring(root, 'unicode')
        with open(self.file_path_for_outcome(outcome), "w") as f:
            f.write(xml)

    def file_path_for_outcome(self, outcome: AssessmentOutcome):
        """
        Build file path for this outcome from state, district, school, and outcome rec id
        Make sure parent folders exist.
        
        :param outcome: 
        :return: 
        """
        path = os.path.join(self.out_path_root,
                            outcome.inst_hierarchy.state.code,
                            outcome.inst_hierarchy.district.id,
                            outcome.inst_hierarchy.school.id)
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, str(outcome.rec_id)) + '.xml'

    def add_examinee_attribute(self, parent, name, value, contextDateStr):
        if value:
            attr = SubElement(parent, 'ExamineeAttribute')
            attr.set('context', 'FINAL')
            attr.set('name', name)
            attr.set('value', str(value))
            attr.set('contextDate', contextDateStr)

    def add_examinee_relationship(self, parent, name, value, contextDateStr):
        if value:
            attr = SubElement(parent, 'ExamineeRelationship')
            attr.set('context', 'FINAL')
            attr.set('name', name)
            attr.set('value', str(value))
            attr.set('contextDate', contextDateStr)

    def add_scale_score(self, parent, measure, scale_score, scale_score_range_min, perf_lvl):
        if scale_score:
            score = SubElement(parent, 'Score')
            score.set('measureOf', measure)
            score.set('measureLabel', 'ScaleScore')
            score.set('value', str(scale_score))
            score.set('standardError', str(scale_score - scale_score_range_min))
            score = SubElement(parent, 'Score')
            score.set('measureOf', measure)
            score.set('measureLabel', 'PerformanceLevel')
            score.set('value', str(perf_lvl))
            score.set('standardError', '')

    def add_score_info(self, parent, dimension, points):
        scoreInfo = SubElement(parent, 'ScoreInfo')
        scoreInfo.set('maxScore', '0')
        scoreInfo.set('scoreDimension', dimension)
        scoreInfo.set('scorePoint', str(points))
        scoreInfo.set('scoreStatus', 'Scored')
        return scoreInfo

    def map_asmt_type(self, value):
        return 'Summative' if 'summative' in value.lower() else 'Interim'

    def map_gender(self, value):
        if 'female' == value.lower(): return 'Female'
        if 'male' == value.lower(): return 'Male'
        if 'non_binary' == value.lower(): return 'NonBinary'
        return None

    def map_yes_no(self, value):
        return 'Yes' if value else 'No'

    def map_advancement(self, student):
        if student.held_back: return 'HeldBack'
        if student.transfer: return 'Transfer'
        return 'Normal'
