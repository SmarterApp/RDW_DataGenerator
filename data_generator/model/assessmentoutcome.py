"""
Model the core of an assessment outcome (an instance of a student taking an assessment).

"""

import datetime

import data_generator.config.cfg as cfg


class AssessmentOutcome:
    """The core assessment outcome class.
    """

    # using slots here only to avoid bugs due to typos etc.
    __slots__ = ('guid student assessment date_taken start_date status_date submit_date '
                 'rec_id inst_hierarchy result_status '
                 'server database client_name status completeness admin_condition session '
                 'overall_score overall_score_range_min overall_score_range_max overall_perf_lvl '
                 'claim_1_score claim_1_score_range_min claim_1_score_range_max claim_1_perf_lvl '
                 'claim_2_score claim_2_score_range_min claim_2_score_range_max claim_2_perf_lvl '
                 'claim_3_score claim_3_score_range_min claim_3_score_range_max claim_3_perf_lvl '
                 'claim_4_score claim_4_score_range_min claim_4_score_range_max claim_4_perf_lvl '
                 'acc_asl_video_embed acc_print_on_demand_items_nonembed acc_noise_buffer_nonembed acc_braile_embed '
                 'acc_closed_captioning_embed acc_text_to_speech_embed acc_abacus_nonembed '
                 'acc_alternate_response_options_nonembed acc_calculator_nonembed acc_multiplication_table_nonembed '
                 'acc_print_on_demand_nonembed acc_read_aloud_nonembed acc_scribe_nonembed acc_speech_to_text_nonembed '
                 'acc_streamline_mode '
                 'from_date to_date item_data'.split())

    def __init__(self):
        self.guid = None  # aka oppId? or key?
        self.student = None
        self.assessment = None
        self.date_taken = None
        self.start_date = None
        self.status_date = None
        self.submit_date = None
        self.rec_id = None
        self.inst_hierarchy = None
        self.result_status = cfg.ASMT_STATUS_ACTIVE
        self.server = 'ip-10-113-148-45'    # TODO - randomly generate?
        self.database = 'session'           # TODO - ?
        self.client_name = 'SBAC'
        self.status = 'scored'              # TODO - should we randomly not score a teeny fraction of them?
        self.completeness = 'Complete'      # TODO - should we have forceComplete, invalid, etc.?
        self.admin_condition = None
        self.session = None
        self.overall_score = None
        self.overall_score_range_min = None
        self.overall_score_range_max = None
        self.overall_perf_lvl = None
        self.claim_1_score = None
        self.claim_1_score_range_min = None
        self.claim_1_score_range_max = None
        self.claim_1_perf_lvl = None
        self.claim_2_score = None
        self.claim_2_score_range_min = None
        self.claim_2_score_range_max = None
        self.claim_2_perf_lvl = None
        self.claim_3_score = None
        self.claim_3_score_range_min = None
        self.claim_3_score_range_max = None
        self.claim_3_perf_lvl = None
        self.claim_4_score = None
        self.claim_4_score_range_min = None
        self.claim_4_score_range_max = None
        self.claim_4_perf_lvl = None
        self.acc_asl_video_embed = 0
        self.acc_print_on_demand_items_nonembed = 0
        self.acc_noise_buffer_nonembed = 0
        self.acc_braile_embed = 0
        self.acc_closed_captioning_embed = 0
        self.acc_text_to_speech_embed = 0
        self.acc_abacus_nonembed = 0
        self.acc_alternate_response_options_nonembed = 0
        self.acc_calculator_nonembed = 0
        self.acc_multiplication_table_nonembed = 0
        self.acc_print_on_demand_nonembed = 0
        self.acc_read_aloud_nonembed = 0
        self.acc_scribe_nonembed = 0
        self.acc_speech_to_text_nonembed = 0
        self.acc_streamline_mode = 0
        self.from_date = cfg.HIERARCHY_FROM_DATE
        self.to_date = datetime.date(9999, 12, 31)
        self.item_data = []

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'state': self.inst_hierarchy.state,
                'district': self.student.school.district,
                'school': self.student.school,
                'student': self.student,
                'institution_hierarchy': self.inst_hierarchy,
                'assessment': self.assessment,
                'assessment_outcome': self}
