"""
Model the core of a subject.

NOTE: there is a bunch of subject metadata in here that isn't actually used.
For example, alt-scoring is loaded and includes the number of performance levels
but during generation, the performance levels are derived from the alt cutpoints
from the assessment definition.
"""


class Subject:
    """The subject class.
    """

    # using slots here only to avoid bugs due to typos etc.
    __slots__ = ('code', 'types', 'overall', 'alts', 'claims',
                 'emit_overall_stderr', 'emit_claim_score', 'sbac_claim_levels', 'el_adjacent')

    def __init__(self, code: str):
        self.code = code        # subject code, e.g. Math, ELA, ELPAC
        self.types = {}         # type -> SubjectAssessmentType for supported types
        self.overall = None     # Scorable
        self.alts = None        # alt scoring Scorables
        self.claims = None      # claim scoring Scorables (only for scorable claims)
        self.emit_overall_stderr = True     # ELPAC scoring doesn't include overall stderr
        self.emit_claim_score = True        # ELPAC scoring doesn't include claim scores
        self.sbac_claim_levels = True       # SmarterBalanced claim levels are 1-3 based on +-1.5 stderr
        self.el_adjacent = False            # ELPAC, ELA are related to english learner


class SubjectAssessmentType:
    """Subject-level assessment type information
    """

    __slots__ = ('code', 'overall_scoring', 'alt_scoring', 'claim_scoring')

    def __init__(self, code: str):
        self.code = code                # assessment type, 'SUM', 'ICA', 'IAB'
        self.overall_scoring = None     # overall SubjectScoring
        self.alt_scoring = None         # alt SubjectScoring
        self.claim_scoring = None       # claim SubjectScoring


class SubjectScoring:
    """Subject-level scoring information for overall, alt or claim scoring
    """

    __slots__ = ('perf_levels', 'min_score', 'max_score')

    def __init__(self, perf_levels: int, min_score: int = None, max_score: int = None):
        self.perf_levels = perf_levels  # number of performance levels
        self.min_score = min_score      # (optional) min score value
        self.max_score = max_score      # (optional) max score value
