"""
A writer producing output like the assessment package tabulator.

"""
import csv

TabulatorFieldNames = [
    'AssessmentId', 'AssessmentName', 'AssessmentSubject', 'AssessmentGrade', 'AssessmentType', 'AssessmentSubtype',
    'AssessmentLabel', 'AssessmentVersion', 'AcademicYear', 'FullItemKey', 'BankKey', 'ItemId', 'Filename', 'Version',
    'ItemType', 'Grade', 'Standard', 'Claim', 'Target', 'PassageRef', 'ASL', 'Braille', 'LanguageBraille', 'DOK',
    'Language', 'AllowCalculator', 'MathematicalPractice', 'MaxPoints', 'Glossary', 'ScoringEngine', 'Spanish',
    'IsFieldTest', 'IsActive', 'ResponseRequired', 'AdminRequired', 'ItemPosition', 'MeasurementModel', 'Weight',
    'ScorePoints', 'a', 'b0_b', 'b1_c', 'b2', 'b3', 'avg_b', 'bpref1', 'bpref2', 'bpref3', 'bpref4', 'bpref5', 'bpref6',
    'bpref7', 'CommonCore', 'ClaimContentTarget', 'SecondaryCommonCore', 'SecondaryClaimContentTarget', 'CutPoint1',
    'ScaledLow1', 'ScaledHigh1', 'CutPoint2', 'ScaledLow2', 'ScaledHigh2', 'CutPoint3', 'ScaledLow3', 'ScaledHigh3',
    'CutPoint4', 'ScaledLow4', 'ScaledHigh4'
]


def write_assessments(file, asmts):
    with open(file, "w") as f:
        writer = csv.DictWriter(f, TabulatorFieldNames)
        writer.writeheader()
        for asmt in asmts:
            writer.writerows(__asmt_to_rows(asmt))


def __asmt_to_rows(asmt):
    row = {
        'AssessmentId': asmt.id,
        'AssessmentName': asmt.name,
        'AssessmentSubject': asmt.subject,
        'AssessmentGrade': asmt.grade,
        'AssessmentType': __map_type(asmt),
        'AssessmentSubtype': __map_subtype(asmt),
        'AssessmentLabel': None,
        'AssessmentVersion': asmt.version,
        'AcademicYear': asmt.year,
        'BankKey': asmt.bank_key,
        'CutPoint1': 1,
        'ScaledLow1': asmt.overall_score_min,
        'ScaledHigh1': asmt.overall_cut_point_1,
        'CutPoint2': 2,
        'ScaledLow2': asmt.overall_cut_point_1,
        'ScaledHigh2': asmt.overall_cut_point_2,
        'CutPoint3': 3,
        'ScaledLow3': asmt.overall_cut_point_2,
        'ScaledHigh3': asmt.overall_cut_point_3,
        'CutPoint4': 4,
        'ScaledLow4': asmt.overall_cut_point_3,
        'ScaledHigh4': asmt.overall_score_max,
    }
    if not asmt.item_bank or len(asmt.item_bank) == 0:
        return [row]

    rows = []
    for item in asmt.item_bank:
        row['BankKey'] = item.bank_key
        row['ItemId'] = item.item_key
        row['FullItemKey'] = str(item.bank_key) + '-' + str(item.item_key)
        row['ItemType'] = item.type
        row['ItemPosition'] = item.position
        row['MaxPoints'] = item.max_score
        row['DOK'] = item.dok
        row['IsFieldTest'] = 'FALSE' if item.operational else 'TRUE'
        row['IsActive'] = 'TRUE'
        rows.append(row.copy())
    return rows


def __map_type(asmt):
    if asmt.type == 'SUMMATIVE': return 'summative'
    return 'interim'


def __map_subtype(asmt):
    if asmt.type == 'SUMMATIVE': return 'SUM'
    if asmt.type == 'INTERIM COMPREHENSIVE': return 'ICA'
    return 'IAB'