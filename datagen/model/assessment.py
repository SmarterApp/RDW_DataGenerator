"""
Model the core of an assessment.
"""

import datagen.config.cfg as cfg
import datagen.writers.datefilters as write_filters


class Assessment:
    """The core assessment class.
    """

    # using slots here only to avoid bugs due to typos etc.
    __slots__ = ('guid', 'id', 'name', 'subject', 'grade', 'contract', 'mode', 'rec_id', 'type', 'year', 'version',
                 'overall', 'alts', 'claims',
                 'from_date', 'to_date', 'effective_date', 'segment', 'accommodations',
                 'item_bank', 'item_total_score')

    def __init__(self):
        self.guid = None
        self.id = None          # conventional SBAC assessment id, e.g. (SBAC)SBAC-Math-8-Winter-2016-2017
        self.name = None        # conventional SBAC assessment name, e.g. SBAC-Math-8
        self.subject = None
        self.grade = None       # integer, KG=0, G1=1, ..., G13=13; doesn't handle HS, UG, PS, etc.
        self.contract = 'SBAC'
        self.mode = 'online'
        self.rec_id = None      # record id, used to link output records
        self.type = None        # SUMMATIVE, INTERIM COMPREHENSIVE, INTERIM ASSESSMENT BLOCK
        self.year = None        # academic year, e.g. 2017 for 2016-2017
        self.version = None
        self.overall = None     # a single Scorable
        self.alts = None        # list of Scorable
        self.claims = None      # list of Scorable
        self.from_date = cfg.HIERARCHY_FROM_DATE
        self.to_date = None
        self.effective_date = None
        self.segment = None
        self.accommodations = set()     # set of allowed accommodations
        self.item_bank = None
        self.item_total_score = None    # cache of sum of item score

    def is_summative(self):
        return 'SUMMATIVE' in self.type

    def is_interim(self):
        return 'INTERIM' in self.type

    def is_iab(self):
        return 'BLOCK' in self.type

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        Root objects made available:
          - assessment

        :returns: Dictionary of root objects
        """
        return {'assessment': self,
                'assessment_effective': {'date': write_filters.filter_date_Ymd(self.effective_date)}}

    # These properties provide backward-compatible getters to claim info which was pushed into a list of objects

    @property
    def claim_1_name(self):
        return self._safe_claim_name(0)

    @property
    def claim_2_name(self):
        return self._safe_claim_name(1)

    @property
    def claim_3_name(self):
        return self._safe_claim_name(2)

    @property
    def claim_4_name(self):
        return self._safe_claim_name(3)

    @property
    def claim_1_score_min(self):
        return self._safe_claim_score_min(0)

    @property
    def claim_2_score_min(self):
        return self._safe_claim_score_min(1)

    @property
    def claim_3_score_min(self):
        return self._safe_claim_score_min(2)

    @property
    def claim_4_score_min(self):
        return self._safe_claim_score_min(3)

    @property
    def claim_1_score_max(self):
        return self._safe_claim_score_max(0)

    @property
    def claim_2_score_max(self):
        return self._safe_claim_score_max(1)

    @property
    def claim_3_score_max(self):
        return self._safe_claim_score_max(2)

    @property
    def claim_4_score_max(self):
        return self._safe_claim_score_max(3)

    def _safe_claim_name(self, i):
        return self.claims[i].name if self.claims and len(self.claims) > i else None

    def _safe_claim_score_min(self, i):
        return self.claims[i].score_min if self.claims and len(self.claims) > i else None

    def _safe_claim_score_max(self, i):
        return self.claims[i].score_max if self.claims and len(self.claims) > i else None
