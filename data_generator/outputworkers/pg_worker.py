import data_generator.config.out as sbac_out_config
import data_generator.writers.writepostgres as postgres_writer
from data_generator.model.assessment import Assessment
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.model.institutionhierarchy import InstitutionHierarchy
from data_generator.model.interimassessmentoutcome import InterimAssessmentOutcome
from data_generator.model.student import Student
from data_generator.outputworkers.worker import Worker


class PgWorker(Worker):
    def __init__(self, host, port, dbname, user, pwd, schema):
        self.db_connection = None
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.pwd = pwd
        self.schema = schema

    def prepare(self):
        self.db_connection = postgres_writer.create_dbcon(self.host, self.port, self.dbname, self.user, self.pwd)

    def cleanup(self):
        if self.db_connection:
            self.db_connection.close()

    def write_assessments(self, asmts: [Assessment]):
        postgres_writer.write_records_to_table(self.db_connection, self.schema + '.dim_asmt', sbac_out_config.DIM_ASMT_FORMAT['columns'], asmts)

    def write_hierarchies(self, hierarchies: [InstitutionHierarchy]):
        postgres_writer.write_records_to_table(self.db_connection, self.schema + '.dim_inst_hier', sbac_out_config.DIM_INST_HIER_FORMAT['columns'], hierarchies)

    def write_students_dim(self, students: [Student]):
        postgres_writer.write_records_to_table(self.db_connection, self.schema + '.dim_student', sbac_out_config.DIM_STUDENT_FORMAT['columns'], students,
                                               entity_filter=('held_back', False))

    def write_students_reg(self, students: [Student], rs_guid, asmt_year):
        postgres_writer.write_records_to_table(self.db_connection, self.schema + '.student_reg', sbac_out_config.STUDENT_REG_FORMAT['columns'], students)

    def write_iab_outcome(self, results: [InterimAssessmentOutcome], guid):
        try:
            postgres_writer.write_records_to_table(self.db_connection, self.schema + '.fact_block_asmt_outcome', sbac_out_config.FBAO_FORMAT['columns'], results)
        except Exception as e:
            print('PostgreSQL EXCEPTION ::: %s' % str(e))

    def write_assessment_outcome(self, results: [AssessmentOutcome], guid, state_code, district_id):
        try:
            postgres_writer.write_records_to_table(self.db_connection, self.schema + '.fact_asmt_outcome_vw',
                                                   sbac_out_config.FAO_VW_FORMAT['columns'], results)
            postgres_writer.write_records_to_table(self.db_connection, self.schema + '.fact_asmt_outcome',
                                                   sbac_out_config.FAO_FORMAT['columns'], results)
        except Exception as e:
            print('PostgreSQL EXCEPTION ::: %s' % str(e))
