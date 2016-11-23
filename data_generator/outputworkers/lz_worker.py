import data_generator.config.out as sbac_out_config
import data_generator.writers.writecsv as csv_writer
import data_generator.writers.writejson as json_writer
from data_generator.model.assessment import Assessment
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.interimassessmentoutcome import InterimAssessmentOutcome
from data_generator.model.registrationsystem import RegistrationSystem
from data_generator.model.student import Student
from data_generator.outputworkers.worker import Worker


class LzWorker(Worker):
    def __init__(self, root_path: str):
        self.root_path = root_path

    def prepare(self):
        csv_writer.clean_dir(self.root_path)

    def write_student_registration_config(self, year: int, rs: RegistrationSystem):
        # Create the JSON file
        file_name = sbac_out_config.REGISTRATION_SYSTEM_FORMAT['name']
        file_name = file_name.replace('<YEAR>', str(year)).replace('<GUID>', rs.guid_sr)
        json_writer.write_object_to_file(file_name, sbac_out_config.REGISTRATION_SYSTEM_FORMAT['layout'], rs, self.root_path)

        # Prepare the SR CSV file
        file_name = sbac_out_config.SR_FORMAT['name'].replace('<YEAR>', str(year)).replace('<GUID>', rs.guid_sr)
        csv_writer.prepare_csv_file(file_name, sbac_out_config.SR_FORMAT['columns'], self.root_path)

    def write_iab(self, asmt: Assessment):
        file_name = sbac_out_config.IAB_JSON_FORMAT['name'].replace('<GUID>', asmt.guid_sr)
        json_writer.write_object_to_file(file_name, sbac_out_config.IAB_JSON_FORMAT['layout'], asmt, self.root_path)

        file_name = sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<GUID>', asmt.guid_sr)
        csv_writer.prepare_csv_file(file_name, sbac_out_config.LZ_REALDATA_FORMAT['columns'], self.root_path)

    def write_assessment(self, asmt: Assessment):
        file_name = sbac_out_config.ASMT_JSON_FORMAT['name'].replace('<GUID>', asmt.guid_sr)
        json_writer.write_object_to_file(file_name, sbac_out_config.ASMT_JSON_FORMAT['layout'], asmt,
                                         root_path=self.root_path)
        file_name = sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<GUID>', asmt.guid_sr)
        csv_writer.prepare_csv_file(file_name, sbac_out_config.LZ_REALDATA_FORMAT['columns'], root_path=self.root_path)

    def write_students_reg(self, students: [Student], out_name):
        csv_writer.write_records_to_file(out_name, sbac_out_config.SR_FORMAT['columns'], students, root_path=self.root_path)

    def write_iab_outcome(self, results: [InterimAssessmentOutcome], guid):
        csv_writer.write_records_to_file(sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<GUID>', guid),
                                         sbac_out_config.LZ_REALDATA_FORMAT['columns'],
                                         results,
                                         root_path=self.root_path,
                                         entity_filter=('result_status', 'C'))

    def write_assessment_outcome(self, results: [AssessmentOutcome], guid):
        csv_writer.write_records_to_file(sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<GUID>', guid),
                                         sbac_out_config.LZ_REALDATA_FORMAT['columns'], results, root_path=self.root_path,
                                         entity_filter=('result_status', 'C'))
