import os

import data_generator.config.out as sbac_out_config
import data_generator.writers.writecsv as csv_writer
from data_generator.model.assessmentoutcome import AssessmentOutcome
from data_generator.outputworkers.worker import Worker
from data_generator.writers.datefilters import FILTERS as DG_FILTERS


class CSVItemLevelDataWorker(Worker):
    def __init__(self, root_path: str):
        self.root_path = root_path

    def write_assessment_outcome(self, results: [AssessmentOutcome], guid, state_code, district_id):
        for sao in results:
            try:
                asmt = sao.assessment
                # Only write out summative item level results
                # TODO: not sure why it is written for summative only
                if asmt.type == 'SUMMATIVE':
                    it_dir_path = os.path.join(state_code, str(asmt.year), asmt.type, DG_FILTERS['date_Ymd'](asmt.effective_date), asmt.subject,
                                               str(sao.student.grade), district_id)
                    it_file_path = os.path.join(it_dir_path, sbac_out_config.LZ_ITEMDATA_FORMAT['name'].replace('<STUDENT_ID>', sao.student.guid_sr))

                    if not os.path.exists(os.path.join(self.root_path, it_dir_path)):
                        os.makedirs(os.path.join(self.root_path, it_dir_path))

                    csv_writer.write_records_to_file(it_file_path, sbac_out_config.LZ_ITEMDATA_FORMAT['columns'], sao.item_data, root_path=self.root_path)
            except Exception as e:
                print('Exception in CSVItemLevelDataWorker ::: %s' % str(e))
