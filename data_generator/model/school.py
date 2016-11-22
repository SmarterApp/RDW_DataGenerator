"""
A school.
"""


class School:
    """A core of a school.
    """

    def __init__(self):
        self.guid = None
        self.name = None
        self.district = None
        self.type_str = None
        self.config = None
        self.demo_config = None
        self.guid_sr = None
        self.takes_interim_asmts = False

    @property
    def grades(self):
        """The grades in the school, ordered low to high.
        """
        return sorted(self.config['grades'])

    @property
    def student_count_min(self):
        """The minimum number of students to have in a grade for this school.
        """
        return self.config['students']['min']

    @property
    def student_count_max(self):
        """The maximum number of students to have in a grade for this school.
        """
        return self.config['students']['max']

    @property
    def student_count_avg(self):
        """The average number of students to have in a grade for this school.
        """
        if 'avg' not in self.config['students']:
            smin, smax = self.config['students']['min'], self.config['students']['max']
            self.config['students']['avg'] = ((smax - smin) // 2) + smin
        return self.config['students']['avg']
