"""
A student being enrolled in a section of a class.
"""


class Enrollment:
    """A student being enrolled in a section.
    """

    def __init__(self):
        self.guid = None
        self.section = None
        self.student = None
        self.grade = None

    def get_object_set(self):
        """Get the set of objects that this exposes to a CSV or JSON writer.

        Root objects made available:
          - state
          - district
          - school
          - student
          - class
          - section
          - enrollment

        :returns: Dictionary of root objects
        """
        return {'state': self.section.clss.school.district.state,
                'district': self.section.clss.school.district,
                'school': self.section.clss.school,
                'student': self.student,
                'class': self.section.clss,
                'section': self.section,
                'enrollment': self}
