from datagen.model.assessment import Assessment
from datagen.model.assessmentoutcome import AssessmentOutcome
from datagen.model.institutionhierarchy import InstitutionHierarchy
from datagen.model.interimassessmentoutcome import InterimAssessmentOutcome
from datagen.model.registrationsystem import RegistrationSystem
from datagen.model.student import Student


class Worker:
    """
    This class defines a common API for an output worker
    """

    def prepare(self):
        """ Any intital work that should be done to prepare a worker
        """
        pass

    def cleanup(self):
        """ Any intital work that should be done to prepare a worker
        """
        pass

    def write_student_registration_config(self, year: int, rs: RegistrationSystem):
        """ write student registration configuration
        """
        pass

    def write_iab(self, asmt: Assessment):
        """ write iab assessments
        This method is called only for generated assessments.
        """
        pass

    def write_assessment(self, asmt: Assessment):
        """ write assessments (summative and ica)
        This method is called only for generated assessments.
        """
        pass

    def write_assessments(self, asmts: [Assessment]):
        """ write assessments (summative, ica and/or iab)
        This method is called only for generated assessments.

        Both this method and the single assessment methods are called; a worker
        may implement either depending on the desired performance profile.
        """
        pass

    def write_hierarchies(self, hierarchies: [InstitutionHierarchy]):
        """ write institution hierarchy
        """
        pass

    def write_students_dim(self, students: [Student]):
        """ write student dimension
        """
        pass

    def write_students_reg(self, students: [Student], rs_guid, asmt_year):
        """ write student registration
        """
        pass

    def write_iab_outcome(self, results: [InterimAssessmentOutcome], assessment_guid):
        """ write iab outcome for the given assessment id
        """
        pass

    def write_assessment_outcome(self, results: [AssessmentOutcome], assessment_guid, state_code, district_id):
        """ write assessment outcome
        """
        pass
