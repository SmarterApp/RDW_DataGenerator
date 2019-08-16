"""
Model the core of a subject.

NOTE: subject definitions contain a lot more data than this. However, much of
the data is derived elsewhere: for example, the min/max scores and performance
levels are derived from the assessment package file. We don't want to waste too
much effort doing validation and self-consistency checks.

To summarize, just get enough metadata to get the job done.
"""


class Subject:
    """The subject class.
    """

    # using slots here only to avoid bugs due to typos etc.
    __slots__ = ('code', 'types', 'overall', 'alts', 'claims',
                 'emit_overall_stderr', 'emit_claim_score', 'sbac_claim_levels', 'el_adjacent')

    def __init__(self, code: str):
        self.code = code        # subject code, e.g. Math, ELA, ELPAC
        self.types = []         # supported assessment types, e.g. 'SUM', 'ICA', 'IAB'
        self.overall = None     # Scorable
        self.alts = None        # alt scoring Scorables
        self.claims = None      # claim scoring Scorables (only for scorable claims)
        self.emit_overall_stderr = True     # ELPAC scoring doesn't include overall stderr
        self.emit_claim_score = True        # ELPAC scoring doesn't include claim scores
        self.sbac_claim_levels = True       # SmarterBalanced claim levels are 1-3 based on +-1.5 stderr
        self.el_adjacent = False            # ELPAC, ELA are related to english learner
