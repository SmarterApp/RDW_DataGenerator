"""
Metadata for a student group
"""

class StudentGroup:
    """
    Metadata for a student group
    """

    __slots__ = ('subject', 'id', 'name')

    def __init__(self, subject: str, id: str, name: str):
        self.subject = subject
        self.id = id
        self.name = name

