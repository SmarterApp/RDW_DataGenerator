"""
A student.
"""


class Student:
    """A student class
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
        self.eth_pacific = False
        self.eth_amer_ind = False
        self.eth_multi = False
        self.eth_none = False
        self.prg_iep = None
        self.prg_sec504 = None
        self.prg_lep = None
        self.prg_econ_disad = None
        self.held_back = False

        self.rec_id = None
        self.rec_id_sr = None
        self.state = None
        self.district = None
        self.reg_sys = None
        self.guid_sr = None
        self.external_ssid = None
        self.external_ssid_sr = None
        self.school_entry_date = None
        self.prg_migrant = None
        self.prg_idea = None
        self.lang_code = None
        self.lang_prof_level = None
        self.lang_title_3_prg = None
        self.prg_lep_entry_date = None
        self.prg_lep_exit_date = None
        self.prg_primary_disability = None
        self.derived_demographic = None
        self.group_1_id = None
        self.group_1_text = None
        self.group_2_id = None
        self.group_2_text = None
        self.group_3_id = None
        self.group_3_text = None
        self.group_4_id = None
        self.group_4_text = None
        self.group_5_id = None
        self.group_5_text = None
        self.group_6_id = None
        self.group_6_text = None
        self.group_7_id = None
        self.group_7_text = None
        self.group_8_id = None
        self.group_8_text = None
        self.group_9_id = None
        self.group_9_text = None
        self.group_10_id = None
        self.group_10_text = None
        self.skip_iab = None

    @property
    def name(self):
        """The full name of student.
        """
        if self.middle_name is not None:
            return self.first_name + ' ' + self.middle_name + ' ' + self.last_name
        else:
            return self.first_name + ' ' + self.last_name

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.
        """
        return {'state': self.state,
                'district': self.district,
                'school': self.school,
                'registration_system': self.reg_sys,
                'student': self}
