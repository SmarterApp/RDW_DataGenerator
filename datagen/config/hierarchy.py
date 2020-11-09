"""
Configuration for the hierarchy generators.
"""

# District sizes : min/max/avg schools per type of district
SML_MIN = 4
SML_MAX = 2 * SML_MIN
SML_AVG = int((SML_MAX + SML_MIN) / 2)

MED_MIN = 5 * SML_MIN  # if small min =  9 then medium min = 40
MED_MAX = 5 * SML_MAX  # if small max = 18 then medium max = 90
MED_AVG = int((MED_MAX + MED_MIN) / 2)

BIG_MIN = 4 * MED_MIN  # if medium min = 40 then big min =  200
BIG_MAX = 4 * MED_MAX  # if medium max = 90 then big max = 450
BIG_AVG = int((BIG_MAX + BIG_MIN) / 2)

# School ratios
BASE_HIGH = 1
BASE_MIDL = 2
BASE_ELEM = 5
# ratios for 'average' schools
NORM_HIGH = 4 * BASE_HIGH
NORM_MIDL = 4 * BASE_MIDL
NORM_ELEM = 4 * BASE_ELEM
# ratios for 'featured' schools (good schools in good districts, poor schools in poor districts)
FEAT_HIGH = 6 * BASE_HIGH
FEAT_MIDL = 6 * BASE_MIDL
FEAT_ELEM = 6 * BASE_ELEM
# ratios for 'other' schools (poor schools in good districts, good schools in poor districts)
OTHR_HIGH = 1 * BASE_HIGH
OTHR_MIDL = 1 * BASE_MIDL
OTHR_ELEM = 1 * BASE_ELEM

VERY_NORM_HIGH = 3 * BASE_HIGH
VERY_NORM_MIDL = 3 * BASE_MIDL
VERY_NORM_ELEM = 3 * BASE_ELEM

VERY_FEAT_HIGH = 7 * BASE_HIGH
VERY_FEAT_MIDL = 7 * BASE_MIDL
VERY_FEAT_ELEM = 7 * BASE_ELEM


SCHOOL_TYPES = {
    'High School':
        {'type': 'High School',
         'grades': [9, 10, 11, 12],
         'students': {'min': 300, 'max': 400, 'avg': 350},
         'group_size': 40
         },
    'Middle School':
        {'type': 'Middle School',
         'grades': [6, 7, 8],
         'students': {'min': 175, 'max': 250, 'avg': 225},
         'group_size': 30
         },
    'Elementary School':
        {'type': 'Elementary School',
         'grades': [0, 1, 2, 3, 4, 5],
         'students': {'min': 75, 'max': 125, 'avg': 100},
         'group_size': 20
         },
    'K12 School':
        {'type': 'K12 School',
         'grades': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         'students': {'min': 100, 'max': 150, 'avg': 125},
         'group_size': 30
         },
    'Poor High School':
        {'type': 'High School',
         'grades': [9, 10, 11, 12],
         'students': {'min': 300, 'max': 400, 'avg': 350},
         'group_size': 50,
         'adjust_pld': -0.45
         },
    'Poor Middle School':
        {'type': 'Middle School',
         'grades': [6, 7, 8],
         'students': {'min': 175, 'max': 250, 'avg': 225},
         'group_size': 40,
         'adjust_pld': -0.5
         },
    'Poor Elementary School':
        {'type': 'Elementary School',
         'grades': [0, 1, 2, 3, 4, 5],
         'students': {'min': 75, 'max': 125, 'avg': 100},
         'group_size': 30,
         'adjust_pld': -0.6
         },
    'Good High School':
        {'type': 'High School',
         'grades': [9, 10, 11, 12],
         'students': {'min': 300, 'max': 400, 'avg': 350},
         'group_size': 30,
         'adjust_pld': 0.35
         },
    'Good Middle School':
        {'type': 'Middle School',
         'grades': [6, 7, 8],
         'students': {'min': 175, 'max': 250, 'avg': 225},
         'group_size': 25,
         'adjust_pld': 0.4
         },
    'Good Elementary School':
        {'type': 'Elementary School',
         'grades': [0, 1, 2, 3, 4, 5],
         'students': {'min': 75, 'max': 125, 'avg': 100},
         'group_size': 15,
         'adjust_pld': 0.5
         },
    'Big High School':
        {'type': 'High School',
         'grades': [9, 10, 11, 12],
         'students': {'min': 600, 'max': 800, 'avg': 700},
         'group_size': 40
         },
    'Big Middle School':
        {'type': 'Middle School',
         'grades': [6, 7, 8],
         'students': {'min': 200, 'max': 400, 'avg': 300},
         'group_size': 30
         },
    'Big Elementary School':
        {'type': 'Elementary School',
         'grades': [0, 1, 2, 3, 4, 5],
         'students': {'min': 100, 'max': 200, 'avg': 150},
         'group_size': 20
         },
    'UDL High School':
        {'type': 'High School',
         'grades': [9, 10, 11, 12],
         'students': {'min': 999, 'max': 1001, 'avg': 1000},
         'group_size': 40
         },
    'Tiny High School':
        {'type': 'High School',
         'grades': [9, 10, 11, 12],
         'students': {'min': 5, 'max': 10, 'avg': 7},
         'group_size': 10
         },
    'Tiny Middle School':
        {'type': 'Middle School',
         'grades': [6, 7, 8],
         'students': {'min': 5, 'max': 10, 'avg': 7},
         'group_size': 10
         },
    'Tiny Elementary School':
        {'type': 'Elementary School',
         'grades': [0, 1, 2, 3, 4, 5],
         'students': {'min': 5, 'max': 10, 'avg': 7},
         'group_size': 10
         },
    'Tiny K12 School':
        {'type': 'K12 School',
         'grades': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         'students': {'min': 5, 'max': 10, 'avg': 7},
         'group_size': 10
         },
    'Demo High School':
        {'type': 'High School',
         'grades': [11],
         'students': {'min': 100, 'max': 200, 'avg': 150},
         'group_size': 30
         },
    'Demo Middle School':
        {'type': 'Middle School',
         'grades': [7],
         'students': {'min': 100, 'max': 200, 'avg': 150},
         'group_size': 30
         },
    'Demo Elementary School':
        {'type': 'Elementary School',
         'grades': [3],
         'students': {'min': 100, 'max': 140, 'avg': 120},
         'group_size': 20
         },
}

DISTRICT_TYPES = {
    'Big Average':
        {'school_counts': {'min': BIG_MIN, 'max': BIG_MAX, 'avg': BIG_AVG},
         'school_types_and_ratios':
             {'High School': NORM_HIGH,
              'Middle School': NORM_MIDL,
              'Elementary School': NORM_ELEM
              }
         },
    'Big Good':
        {'school_counts': {'min': BIG_MIN, 'max': BIG_MAX, 'avg': BIG_AVG},
         'school_types_and_ratios':
             {'High School': NORM_HIGH,
              'Middle School': NORM_MIDL,
              'Elementary School': NORM_ELEM,
              'Good High School': FEAT_HIGH,
              'Good Middle School': FEAT_MIDL,
              'Good Elementary School': FEAT_ELEM,
              'Poor High School': OTHR_HIGH,
              'Poor Middle School': OTHR_MIDL,
              'Poor Elementary School': OTHR_ELEM
              }
         },
    'Big Poor':
        {'school_counts': {'min': BIG_MIN, 'max': BIG_MAX, 'avg': BIG_AVG},
         'school_types_and_ratios':
             {'High School': NORM_HIGH,
              'Middle School': NORM_MIDL,
              'Elementary School': NORM_ELEM,
              'Poor High School': FEAT_HIGH,
              'Poor Middle School': FEAT_MIDL,
              'Poor Elementary School': FEAT_ELEM,
              'Good High School': OTHR_HIGH,
              'Good Middle School': OTHR_MIDL,
              'Good Elementary School': OTHR_ELEM
              }
         },
    'Big LA':
        {'school_counts': {'min': 1100, 'max': 1200, 'avg': 1150},
         'school_types_and_ratios':
             {'Big High School': NORM_HIGH,
              'Big Middle School': NORM_MIDL,
              'Big Elementary School': NORM_ELEM
              }
         },
    'Medium Average':
        {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},
         # if SML_MIN = 9 then (40, 90, 65)
         'school_types_and_ratios':
             {'High School': NORM_HIGH,
              'Middle School': NORM_MIDL,
              'Elementary School': NORM_ELEM
              }
         },
    'Medium Good':
        {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},
         'school_types_and_ratios':
             {'High School': NORM_HIGH,
              'Middle School': NORM_MIDL,
              'Elementary School': NORM_ELEM,
              'Good High School': FEAT_HIGH,
              'Good Middle School': FEAT_MIDL,
              'Good Elementary School': FEAT_ELEM,
              'Poor High School': OTHR_HIGH,
              'Poor Middle School': OTHR_MIDL,
              'Poor Elementary School': OTHR_ELEM
              }
         },
    'Medium Very Good':
        {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},
         'school_types_and_ratios':
             {'High School': VERY_NORM_HIGH,
              'Middle School': VERY_NORM_MIDL,
              'Elementary School': VERY_NORM_ELEM,
              'Good High School': VERY_FEAT_HIGH,
              'Good Middle School': VERY_FEAT_MIDL,
              'Good Elementary School': VERY_FEAT_ELEM
              }
         },
    'Medium Very Poor':
        {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},
         'school_types_and_ratios':
             {'High School': VERY_NORM_HIGH,
              'Middle School': VERY_NORM_MIDL,
              'Elementary School': VERY_NORM_ELEM,
              'Poor High School': VERY_FEAT_HIGH,
              'Poor Middle School': VERY_FEAT_MIDL,
              'Poor Elementary School': VERY_FEAT_ELEM
              }
         },
    'Medium Poor':
        {'school_counts': {'min': MED_MIN, 'max': MED_MAX, 'avg': MED_AVG},
         'school_types_and_ratios':
             {'High School': NORM_HIGH,
              'Middle School': NORM_MIDL,
              'Elementary School': NORM_ELEM,
              'Poor High School': FEAT_HIGH,
              'Poor Middle School': FEAT_MIDL,
              'Poor Elementary School': FEAT_ELEM,
              'Good High School': OTHR_HIGH,
              'Good Middle School': OTHR_MIDL,
              'Good Elementary School': OTHR_ELEM
              }
         },
    'Small Average':
        {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
         # if SML_MIN = 9 then (9, 18, 13)
         'school_types_and_ratios':
             {'High School': NORM_HIGH,
              'Big Middle School': NORM_MIDL,
              'Elementary School': NORM_ELEM
              }
         },
    'Small Good':
        {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
         'school_types_and_ratios':
             {'High School': NORM_HIGH,
              'Middle School': NORM_MIDL,
              'Elementary School': NORM_ELEM,
              'Good High School': FEAT_HIGH,
              'Good Middle School': FEAT_MIDL,
              'Good Elementary School': FEAT_ELEM,
              'Poor High School': OTHR_HIGH,
              'Poor Middle School': OTHR_MIDL,
              'Poor Elementary School': OTHR_ELEM
              }
         },
    'Small Very Good':
        {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
         'school_types_and_ratios':
             {'High School': VERY_NORM_HIGH,
              'Middle School': VERY_NORM_MIDL,
              'Elementary School': VERY_NORM_ELEM,
              'Good High School': VERY_FEAT_HIGH,
              'Good Middle School': VERY_FEAT_MIDL,
              'Good Elementary School': VERY_FEAT_ELEM
              }
         },
    'Small Very Poor':
        {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
         'school_types_and_ratios':
             {'High School': VERY_NORM_HIGH,
              'Middle School': VERY_NORM_MIDL,
              'Elementary School': VERY_NORM_ELEM,
              'Poor High School': VERY_FEAT_HIGH,
              'Poor Middle School': VERY_FEAT_MIDL,
              'Poor Elementary School': VERY_FEAT_ELEM
              }
         },
    'Small Poor':
        {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
         'school_types_and_ratios': {'High School': NORM_HIGH,
                                     'Middle School': NORM_MIDL,
                                     'Elementary School': NORM_ELEM,
                                     'Poor High School': FEAT_HIGH,
                                     'Poor Middle School': FEAT_MIDL,
                                     'Poor Elementary School': FEAT_ELEM,
                                     'Good High School': OTHR_HIGH,
                                     'Good Middle School': OTHR_MIDL,
                                     'Good Elementary School': OTHR_ELEM
                                     }
         },
    'Big UDL':
        {'school_counts': {'min': 200, 'max': 201, 'avg': 200},
         'school_types_and_ratios': {'UDL High School': 1}
         },
    'Tiny':
        {'school_counts': {'min': SML_MIN, 'max': SML_MAX, 'avg': SML_AVG},
         'school_types_and_ratios':
             {'Tiny High School': NORM_HIGH,
              'Tiny Middle School': NORM_MIDL,
              'Tiny Elementary School': NORM_ELEM
              }
         },
    'Demo':
        {'school_counts': {'min': 3, 'max': 3, 'avg': 3},
         'school_types_and_ratios':
             {'Demo High School': 1,
              'Demo Middle School': 1,
              'Demo Elementary School': 1
              }
         },
}
