"""
Model the core of an assessment.
"""

import datagen.config.cfg as cfg


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
        self.subject = None     # the Subject associated with this assessment
        self.grade = None       # integer, KG=0, G1=1, ..., G13=13; doesn't handle HS, UG, PS, etc.
        self.contract = 'SBAC'
        self.mode = 'online'
        self.rec_id = None      # record id, used to link output records
        self.type = None        # SUM, ICA, IAB
        self.year = None        # academic year, e.g. 2017 for 2016-2017
        self.version = None
        self.overall = None     # a single Scorable
        self.alts = None        # (optional) list of Scorable
        self.claims = None      # (optional) list of Scorable
        self.from_date = cfg.HIERARCHY_FROM_DATE
        self.to_date = None
        self.effective_date = None
        self.segment = None
        self.accommodations = set()     # set of allowed accommodations
        self.item_bank = None
        self.item_total_score = None    # cache of sum of item score

    def is_summative(self):
        return 'SUM' == self.type

    def is_interim(self):
        return 'ICA' == self.type

    def is_iab(self):
        return 'IAB' == self.type
