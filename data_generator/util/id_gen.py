"""
Generate IDs that conform to student registration (SBAC) requirements.

"""

import multiprocessing
from uuid import uuid4


class IDGen():
    def __init__(self, lock=multiprocessing.Lock()):
        self._rec_id_lock = lock
        self._rec_id_dict = {}

    def __get_next_rec_id(self, type_str, init=1000000000, inc=1):
        """
        Safely get the next id.

        :param type_str: label for id, e.g. 'student'
        :param init: initial value for id
        :param inc: id increment
        :return: next id
        """
        with self._rec_id_lock:
            if type_str not in self._rec_id_dict:
                self._rec_id_dict[type_str] = init
            nid = self._rec_id_dict[type_str]
            self._rec_id_dict[type_str] += inc
        return nid

    def get_rec_id(self, type_str):
        """
        Get the next integer record ID within the system for the given type string.

        @param type_str: The type string to get a record ID for
        @returns: Next ID for the given type string
        """
        return self.__get_next_rec_id(type_str)

    def get_group_id(self, type_str):
        """
        Helper to get group id: starts at 100 and increments by 100.

        @param type_str: The type string to get a record ID for
        @returns: Next ID for the given type string
        """
        return self.__get_next_rec_id(type_str, 100, 100)

    def get_district_id(self, state_id):
        """
        Get the next district id, based on next record id for districts.
        The format is consistent with the NCES LEA ID scheme: LEA has a 7 digit id which consists
        of the 2 digit state code and a 5 digit unique-within-state id. The school id consists of
        the 7 digit district id and a 5 digit unique-with-district id. Because leading zeroes are
        allowed, we must force the formatting.

        :param state_id: district's state's id
        :return: next district id
        """
        return "{s}{d:05}".format(s=state_id, d=self.__get_next_rec_id(state_id, 1))

    def get_school_id(self, district_id):
        """
        Get the next school id. For NCES, the school id is the district id plus a 5 digit number.

        :param district_id: school's district's id
        :return: next school id
        """
        school_id = self.__get_next_rec_id(district_id, 1)

        # some legacy district ids have the 7 trailing 0's
        # for those, strip the trailing 0's and use a 7-digit format for the school id part
        if len(district_id) > 12 and district_id[-7:] == '0000000':
            return "{d}{s:07}".format(d=district_id[0:-7], s=school_id)
        else:
            return "{d}{s:05}".format(d=district_id, s=school_id)

    @staticmethod
    def get_uuid():
        """
        Get a UUID.

        @returns: New UUID
        """
        return str(uuid4())

    @staticmethod
    def get_sr_uuid():
        """
        Get a UUID that conforms to student registration requirements.

        @returns: New UUID for student registration
        """
        return uuid4().hex[:30]
