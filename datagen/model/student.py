"""
A student.
"""
from datagen.model.studentgroup import StudentGroup


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
        self.military_connected = None
        self.derived_demographic = None
        self.groups = []
        self.capability = {}        # map of subject_code -> capability, 0.0 <= value < 4.0

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

    def set_group(self, new_group: StudentGroup):
        """Sets the student group; enforces one per subject

        :param new_group: student group
        """
        for i, group in enumerate(self.groups):
            if group.subject_code == new_group.subject_code:
                self.groups[i] = new_group
                return
        self.groups.append(new_group)

    def get_group(self, subject_code: str):
        for group in self.groups:
            if group.subject_code == subject_code:
                return group
        return None
