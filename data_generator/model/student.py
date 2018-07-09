"""
A student.
"""
from data_generator.model.studentgroup import StudentGroup


class Student:
    """A student
    """

    def __init__(self):
        self.guid = None
        self.school = None
        self.grade = None
        self.gender = None
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.dob = None
        self.email = None
        self.address_line_1 = None
        self.address_line_2 = None
        self.address_city = None
        self.address_zip = None
        self.eth_white = False
        self.eth_black = False
        self.eth_hispanic = False
        self.eth_asian = False
        self.eth_filipino = False
        self.eth_pacific = False
        self.eth_amer_ind = False
        self.eth_multi = False
        self.eth_none = False
        self.prg_iep = None
        self.prg_sec504 = None
        self.prg_lep = None
        self.prg_econ_disad = None
        self.held_back = False
        self.transfer = False

        self.id = None              # unique natural id for student (ssid)
        self.external_ssid = None
        self.rec_id = None          # record id, used to link output records
        self.state = None
        self.district = None
        self.reg_sys = None
        self.school_entry_date = None
        self.prg_migrant = None
        self.prg_idea = None
        self.lang_code = None
        self.lang_prof_level = None
        self.lang_title_3_prg = None
        self.prg_lep_entry_date = None
        self.prg_lep_exit_date = None
        self.elas = None
        self.elas_start_date = None
        self.prg_primary_disability = None
        self.derived_demographic = None
        self.groups = []
        self.capability = {}        # map of subject -> capability, 0.0 <= value < 4.0

    @property
    def name(self):
        """The full name of student.
        """
        if self.middle_name is not None:
            return self.first_name + ' ' + self.middle_name + ' ' + self.last_name
        else:
            return self.first_name + ' ' + self.last_name

    def reset_ethnicity(self):
        """Clears all the ethnicity fields, setting them false
        """
        self.eth_white = False
        self.eth_black = False
        self.eth_hispanic = False
        self.eth_asian = False
        self.eth_filipino = False
        self.eth_pacific = False
        self.eth_amer_ind = False
        self.eth_multi = False
        self.eth_none = False

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.
        """
        return {'state': self.state,
                'district': self.district,
                'school': self.school,
                'registration_system': self.reg_sys,
                'student': self}

    def set_group(self, new_group: StudentGroup):
        """Sets the student group; enforces one per subject

        :param new_group: student group
        """
        for i, group in enumerate(self.groups):
            if group.subject == new_group.subject:
                self.groups[i] = new_group
                return
        self.groups.append(new_group)

    def get_group(self, subject: str):
        for group in self.groups:
            if group.subject == subject:
                return group
        return None

    # These properties provide backward-compatible getters to group info which was pushed into a list of objects

    @property
    def group_1_id(self): return self._safe_group_id(0)

    @property
    def group_1_text(self): return self._safe_group_name(0)

    @property
    def group_2_id(self): return self._safe_group_id(1)

    @property
    def group_2_text(self): return self._safe_group_name(1)

    @property
    def group_3_id(self): return self._safe_group_id(2)

    @property
    def group_3_text(self): return self._safe_group_name(2)

    @property
    def group_4_id(self): return self._safe_group_id(3)

    @property
    def group_4_text(self): return self._safe_group_name(3)

    @property
    def group_5_id(self): return self._safe_group_id(4)

    @property
    def group_5_text(self): return self._safe_group_name(4)

    @property
    def group_6_id(self): return self._safe_group_id(5)

    @property
    def group_6_text(self): return self._safe_group_name(5)

    @property
    def group_7_id(self): return self._safe_group_id(6)

    @property
    def group_7_text(self): return self._safe_group_name(6)

    @property
    def group_8_id(self): return self._safe_group_id(7)

    @property
    def group_8_text(self): return self._safe_group_name(7)

    @property
    def group_9_id(self): return self._safe_group_id(8)

    @property
    def group_9_text(self): return self._safe_group_name(8)

    @property
    def group_10_id(self): return self._safe_group_id(9)

    @property
    def group_10_text(self): return self._safe_group_name(9)

    def _safe_group_id(self, i):
        return self.groups[i].id if self.groups and len(self.groups) > i else None

    def _safe_group_name(self, i):
        return self.groups[i].name if self.groups and len(self.groups) > i else None
