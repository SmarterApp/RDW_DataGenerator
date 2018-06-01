"""
Model the core of an assessment outcome (an instance of a student taking an assessment).

"""

import data_generator.config.cfg as cfg


class AssessmentOutcome:
    """The core assessment outcome class.
    """

    # using slots here only to avoid bugs due to typos etc.
    __slots__ = ('guid student assessment date_taken start_date status_date submit_date '
                 'rec_id school result_status '
                 'server database client_name status completeness admin_condition session '
                 'overall_score overall_score_range_min overall_score_range_max overall_perf_lvl claim_scores '
                 'acc_asl_video_embed acc_print_on_demand_items_nonembed acc_noise_buffer_nonembed acc_braile_embed '
                 'acc_closed_captioning_embed acc_text_to_speech_embed acc_abacus_nonembed '
                 'acc_alternate_response_options_nonembed acc_calculator_nonembed acc_multiplication_table_nonembed '
                 'acc_print_on_demand_nonembed acc_read_aloud_nonembed acc_scribe_nonembed acc_speech_to_text_nonembed '
                 'acc_streamline_mode from_date to_date accommodations item_data'.split())

    def __init__(self):
        self.guid = None
        self.student = None
        self.assessment = None
        self.date_taken = None
        self.start_date = None
        self.status_date = None
        self.submit_date = None
        self.rec_id = None
        self.school = None
        self.result_status = cfg.ASMT_STATUS_ACTIVE
        self.server = 'ip-10-113-148-45'
        self.database = 'session'
        self.client_name = 'SBAC'
        self.status = 'scored'
        self.completeness = 'Complete'
        self.admin_condition = None
        self.session = None
        self.overall_score = None
        self.overall_score_range_min = None
        self.overall_score_range_max = None
        self.overall_perf_lvl = None
        self.claim_scores = None      # list of ClaimScore's
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
        self.to_date = cfg.HIERARCHY_TO_DATE
        self.accommodations = []    # list of (type, code, value), e.g. ('Calculator', 'TDS_Calc0', 'None')
        self.item_data = []

    def get_object_set(self):
        """
        Get the set of objects that this exposes to a CSV or JSON writer.

        @returns: Dictionary of root objects
        """
        return {'state': self.school.district.state,
                'district': self.school.district,
                'school': self.school,
                'student': self.student,
                'assessment': self.assessment,
                'assessment_outcome': self}

    # These properties provide backward-compatible getters to claim info which was pushed into a list of objects

    @property
    def claim_1_score(self):
        return self._safe_claim_score(0)

    @property
    def claim_2_score(self):
        return self._safe_claim_score(1)

    @property
    def claim_3_score(self):
        return self._safe_claim_score(2)

    @property
    def claim_4_score(self):
        return self._safe_claim_score(3)

    @property
    def claim_1_perf_lvl(self):
        return self._safe_claim_perf_lvl(0)

    @property
    def claim_2_perf_lvl(self):
        return self._safe_claim_perf_lvl(1)

    @property
    def claim_3_perf_lvl(self):
        return self._safe_claim_perf_lvl(2)

    @property
    def claim_4_perf_lvl(self):
        return self._safe_claim_perf_lvl(3)

    @property
    def claim_1_score_range_min(self):
        return self._safe_claim_score_range_min(0)

    @property
    def claim_2_score_range_min(self):
        return self._safe_claim_score_range_min(1)

    @property
    def claim_3_score_range_min(self):
        return self._safe_claim_score_range_min(2)

    @property
    def claim_4_score_range_min(self):
        return self._safe_claim_score_range_min(3)

    @property
    def claim_1_score_range_max(self):
        return self._safe_claim_score_range_max(0)

    @property
    def claim_2_score_range_max(self):
        return self._safe_claim_score_range_max(1)

    @property
    def claim_3_score_range_max(self):
        return self._safe_claim_score_range_max(2)

    @property
    def claim_4_score_range_max(self):
        return self._safe_claim_score_range_max(3)

    def _safe_claim_score(self, i):
            return self.claim_scores[i].score if self.claim_scores and len(self.claim_scores) > i else None

    def _safe_claim_perf_lvl(self, i):
            return self.claim_scores[i].perf_level if self.claim_scores and len(self.claim_scores) > i else None

    def _safe_claim_score_range_min(self, i):
        return self.claim_scores[i].range_min if self.claim_scores and len(self.claim_scores) > i else None

    def _safe_claim_score_range_max(self, i):
        return self.claim_scores[i].range_max if self.claim_scores and len(self.claim_scores) > i else None

