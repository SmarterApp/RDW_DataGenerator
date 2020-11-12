"""
Model the core of an assessment outcome (an instance of a student taking an assessment).

"""

import datagen.config.cfg as cfg


class AssessmentOutcome:
    """The core assessment outcome class.
    """

    # using slots here only to avoid bugs due to typos etc.
    __slots__ = ('guid student assessment date_taken start_date status_date submit_date '
                 'rec_id school result_status '
                 'server database client_name status completeness admin_condition session '
                 'overall alt_scores claim_scores trait_scores target_scores '
                 'acc_asl_video_embed acc_print_on_demand_items_nonembed acc_noise_buffer_nonembed '
                 'acc_braile_embed acc_closed_captioning_embed acc_text_to_speech_embed acc_abacus_nonembed '
                 'acc_alternate_response_options_nonembed acc_calculator_nonembed acc_multiplication_table_nonembed '
                 'acc_print_on_demand_nonembed acc_read_aloud_nonembed acc_scribe_nonembed '
                 'acc_speech_to_text_nonembed acc_streamline_mode from_date to_date accommodations item_data'.split())

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
        self.overall = None             # single overall Score
        self.alt_scores = None          # list of Scores
        self.claim_scores = None        # list of Scores
        self.trait_scores = None        # list of Scores (not great but good enough)
        self.target_scores = None       # list of TargetScores
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
