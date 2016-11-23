import data_generator.config.out as sbac_out_config
import data_generator.writers.writecsv as csv_writer
from data_generator.model.assessment import Assessment
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.institutionhierarchy import InstitutionHierarchy
from data_generator.model.interimassessmentoutcome import InterimAssessmentOutcome
from data_generator.model.student import Student
from data_generator.outputworkers.worker import Worker
from data_generator.writers.datefilters import FILTERS as DATE_TIME_FILTERS
from data_generator.writers.filters import SBAC_FILTERS as FILTERS

csv_writer.register_filters(FILTERS)
csv_writer.register_filters(DATE_TIME_FILTERS)


class CSVStarWorker(Worker):
    def __init__(self, root_path: str):
        self.root_path = root_path

    def prepare(self):
        # Prepare star-schema output files
        csv_writer.prepare_csv_file(sbac_out_config.FAO_VW_FORMAT['name'], sbac_out_config.FAO_VW_FORMAT['columns'], self.root_path)
        csv_writer.prepare_csv_file(sbac_out_config.FAO_FORMAT['name'], sbac_out_config.FAO_FORMAT['columns'], self.root_path)
        csv_writer.prepare_csv_file(sbac_out_config.FBAO_FORMAT['name'], sbac_out_config.FBAO_FORMAT['columns'], self.root_path)
        csv_writer.prepare_csv_file(sbac_out_config.DIM_STUDENT_FORMAT['name'], sbac_out_config.DIM_STUDENT_FORMAT['columns'], self.root_path)
        csv_writer.prepare_csv_file(sbac_out_config.DIM_INST_HIER_FORMAT['name'], sbac_out_config.DIM_INST_HIER_FORMAT['columns'], self.root_path)
        csv_writer.prepare_csv_file(sbac_out_config.DIM_ASMT_FORMAT['name'], sbac_out_config.DIM_ASMT_FORMAT['columns'], self.root_path)
        csv_writer.prepare_csv_file(sbac_out_config.SR_FORMAT['name'], sbac_out_config.SR_FORMAT['columns'], self.root_path)

    def write_iab(self, asmt: Assessment):
        file_name = sbac_out_config.DIM_ASMT_FORMAT['name']
        csv_writer.write_records_to_file(file_name, sbac_out_config.DIM_ASMT_FORMAT['columns'], [asmt], tbl_name='dim_asmt', root_path=self.root_path)

    def write_assessment(self, asmt: Assessment):
        file_name = sbac_out_config.DIM_ASMT_FORMAT['name']
        csv_writer.write_records_to_file(file_name, sbac_out_config.DIM_ASMT_FORMAT['columns'], [asmt], tbl_name='dim_asmt', root_path=self.root_path)

    def write_hierarchies(self, hierarchies: InstitutionHierarchy):
        csv_writer.write_records_to_file(sbac_out_config.DIM_INST_HIER_FORMAT['name'],
                                         sbac_out_config.DIM_INST_HIER_FORMAT['columns'], hierarchies,
                                         tbl_name='dim_hier', root_path=self.root_path)

    def write_students_dim(self, students: [Student]):
        csv_writer.write_records_to_file(sbac_out_config.DIM_STUDENT_FORMAT['name'],
                                         sbac_out_config.DIM_STUDENT_FORMAT['columns'], students,
                                         entity_filter=('held_back', False), tbl_name='dim_student',
                                         root_path=self.root_path)

    def write_students_reg(self, students: [Student], out_name=None):
        csv_writer.write_records_to_file(sbac_out_config.STUDENT_REG_FORMAT['name'],
                                         sbac_out_config.STUDENT_REG_FORMAT['columns'],
                                         students, tbl_name='student_reg',
                                         root_path=self.root_path)

    def write_iab_outcome(self, results: [InterimAssessmentOutcome], guid):
        csv_writer.write_records_to_file(sbac_out_config.FBAO_FORMAT['name'], sbac_out_config.FBAO_FORMAT['columns'], results,
                                         tbl_name='fact_block_asmt_outcome', root_path=self.root_path)

    def write_assessment_outcome(self, results: [AssessmentOutcome], guid):
        csv_writer.write_records_to_file(sbac_out_config.FAO_VW_FORMAT['name'], sbac_out_config.FAO_VW_FORMAT['columns'], results,
                                         tbl_name='fact_asmt_outcome_vw', root_path=self.root_path)
        csv_writer.write_records_to_file(sbac_out_config.FAO_FORMAT['name'], sbac_out_config.FAO_FORMAT['columns'], results,
                                         tbl_name='fact_asmt_outcome', root_path=self.root_path)
