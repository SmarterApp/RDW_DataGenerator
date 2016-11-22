"""
Configuration for state types
"""

STATE_TYPES = {
    'california':
        {'district_types_and_counts': [('Big LA', 1),
                                       ('Big Average', 10),
                                       ('Big Poor', 10),
                                       ('Big Good', 10),
                                       ('Medium Average', 90),
                                       ('Medium Poor', 35),
                                       ('Medium Good', 35),
                                       ('Medium Very Poor', 35),
                                       ('Medium Very Good', 35),
                                       ('Small Average', 200),
                                       ('Small Poor', 150),
                                       ('Small Good', 100),
                                       ('Small Very Poor', 200),
                                       ('Small Very Good', 100)],
         'subject_skip_percentages': {'Math': .04, 'ELA': .03},
         'demographics': 'california'
         },
    'example':
        {'district_types_and_counts': [('Big Average', 1),
                                       ('Medium Average', 1),
                                       ('Medium Poor', 1),
                                       ('Medium Good', 1),
                                       ('Small Average', 5),
                                       ('Small Poor', 2),
                                       ('Small Good', 2)],
         'subject_skip_percentages': {'Math': .04, 'ELA': .03},
         'demographics': 'california'
         },
    'devel':
        {'district_types_and_counts': [('Small Average', 4)],
         'subject_skip_percentages': {'Math': .04, 'ELA': .03},
         'demographics': 'california'
         },
    'tiny':
        {'district_types_and_counts': [('Tiny', 2)],
         'subject_skip_percentages': {'Math': .04, 'ELA': .03},
         'demographics': 'california'
         },
    'udl_test':
        {'district_types_and_counts': [('Big UDL', 1)],
         'subject_skip_percentages': {'Math': 0, 'ELA': 0},
         'demographics': 'california'
         },
    'pa':
        {'district_types_and_counts': [('Big Average', 10),
                                       ('Big Good', 10),
                                       ('Big Poor', 10),
                                       ('Medium Average', 12),
                                       ('Medium Poor', 12),
                                       ('Medium Very Poor', 12),
                                       ('Medium Good', 12),
                                       ('Small Average', 8),
                                       ('Small Poor', 8),
                                       ('Small Good', 8)],
         'subject_skip_percentages': {'Math': .04, 'ELA': .03},
         'demographics': 'california'
         },
}
