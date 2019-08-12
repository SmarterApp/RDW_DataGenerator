"""
Metadata for a student group
"""


class StudentGroup:
    """
    Metadata for a student group
    """

    __slots__ = ('subject_code', 'id', 'name')

    def __init__(self, subject_code: str, id: str, name: str):
        self.subject_code = subject_code
        self.id = id
        self.name = name
