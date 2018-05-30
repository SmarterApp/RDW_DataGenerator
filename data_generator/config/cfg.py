"""
The input configuration for the SBAC RDW project.
"""

import datetime

from data_generator.util.assessment_stats import Properties, Stats, GradeLevels, DemographicLevels

HIERARCHY_FROM_DATE = datetime.date(2014, 9, 1)
HIERARCHY_TO_DATE = datetime.date(9999, 12, 31)

LEP_LANGUAGE_CODES = ['esp', 'fre', 'ben', 'ger', 'chi', 'kor', 'jpn', 'rus']
LEP_PROFICIENCY_LEVELS = ['very poor', 'poor', 'adequate', 'good', 'very good']
LEP_PROFICIENCY_LEVELS_EXIT = ['good', 'very good']
LEP_TITLE_3_PROGRAMS = [None, None,  # Allow blanks and give them higher weight
                        'DualLanguage', 'TwoWayImmersion', 'TransitionalBilingual', 'DevelopmentalBilingual',
                        'HeritageLanguage', 'ShelteredEnglishInstruction', 'StructuredEnglishImmersion', 'SDAIE',
                        'ContentBasedESL', 'PullOutESL', 'Other']
LEP_HAS_ENTRY_DATE_RATE = .9

# CEDS codes: https://ceds.ed.gov/v6/element/000218
PRG_DISABILITY_TYPES = [None, None,  # Allow blanks and give them higher weight
                        'AUT', 'DB', 'DD', 'EMN', 'HI', 'ID', 'MD', 'OI', 'OHI', 'SLD', 'SLI', 'TBI', 'VI']

HAS_ASMT_RESULT_IN_SR_FILE_RATE = .985  # The rate at which students with assessment results are in the SR CSV file

SUBJECTS = ['ELA', 'Math']

# for the FROM_DATE use 8/15 of the assessment year (minus one)
ASMT_TO_DATE = datetime.date(9999, 12, 31)

ASMT_ITEM_BANK_SIZE = 130
IAB_ITEM_BANK_SIZE = 20
ASMT_ITEM_BANK_FORMAT = ['MC', 'EQ', 'MS', 'GI']
ITEMS_PER_ASMT = 100

INTERIM_ASMT_RATE = .85
ASMT_SKIP_RATE = .05
ASMT_RETAKE_RATE = .01
ASMT_DELETE_RATE = .02
ASMT_UPDATE_RATE = .02

ASMT_STATUS_ACTIVE = 'C'
ASMT_STATUS_INACTIVE = 'I'
ASMT_STATUS_DELETED = 'D'

ASMT_VERSION = 'V1'

ASMT_PERF_LEVEL_NAME_1 = 'Minimal Understanding'
ASMT_PERF_LEVEL_NAME_2 = 'Partial Understanding'
ASMT_PERF_LEVEL_NAME_3 = 'Adequate Understanding'
ASMT_PERF_LEVEL_NAME_4 = 'Thorough Understanding'
ASMT_PERF_LEVEL_NAME_5 = None

CLAIM_PERF_LEVEL_NAME_1 = 'Below Standard'
CLAIM_PERF_LEVEL_NAME_2 = 'At/Near Standard'
CLAIM_PERF_LEVEL_NAME_3 = 'Above Standard'

# for each subject and grade, the LOSS, CP12, CP23, CP34, HOSS
ASMT_SCALE_SCORE = {
    'Math': {
        3:  [2189, 2381, 2436, 2501, 2621],
        4:  [2204, 2411, 2485, 2549, 2659],
        5:  [2219, 2455, 2528, 2579, 2700],
        6:  [2235, 2473, 2552, 2610, 2748],
        7:  [2250, 2484, 2567, 2635, 2778],
        8:  [2265, 2504, 2586, 2653, 2802],
        11: [2280, 2543, 2628, 2718, 2862]
    },
    'ELA': {
        3:  [2114, 2367, 2432, 2490, 2623],
        4:  [2131, 2416, 2473, 2533, 2663],
        5:  [2201, 2442, 2502, 2582, 2701],
        6:  [2210, 2457, 2531, 2618, 2724],
        7:  [2258, 2479, 2552, 2649, 2745],
        8:  [2288, 2487, 2567, 2668, 2769],
        11: [2299, 2493, 2583, 2682, 2795]
    }
}

CLAIM_DEFINITIONS = {'Math': [{'name': 'Concepts & Procedures', 'weight': .4},
                              {'name': 'Problem Solving and Modeling & Data Analysis', 'weight': .45},
                              {'name': 'Communicating Reasoning', 'weight': .15}],
                     'ELA': [{'name': 'Reading', 'weight': .20},
                             {'name': 'Writing', 'weight': .25},
                             {'name': 'Listening', 'weight': .25},
                             {'name': 'Research & Inquiry', 'weight': .30}]
                     }

# Legacy accommodations handling in the data generator involves randomly assigning settings to the outcomes
LEGACY_ACCOMMODATIONS = {  # 0: range is 0; 4: range is 4-26
    'acc_abacus_nonembed': {'ELA': 0, 'Math': 4},
    'acc_alternate_response_options_nonembed': {'ELA': 4, 'Math': 4},
    'acc_asl_video_embed': {'ELA': 4, 'Math': 4},
    'acc_braile_embed': {'ELA': 4, 'Math': 4},
    'acc_calculator_nonembed': {'ELA': 0, 'Math': 4},
    'acc_closed_captioning_embed': {'ELA': 4, 'Math': 0},
    'acc_multiplication_table_nonembed': {'ELA': 0, 'Math': 4},
    'acc_noise_buffer_nonembed': {'ELA': 4, 'Math': 4},
    'acc_print_on_demand_items_nonembed': {'ELA': 4, 'Math': 4},
    'acc_print_on_demand_nonembed': {'ELA': 4, 'Math': 4},
    'acc_read_aloud_nonembed': {'ELA': 4, 'Math': 0},
    'acc_scribe_nonembed': {'ELA': 4, 'Math': 0},
    'acc_speech_to_text_nonembed': {'ELA': 4, 'Math': 0},
    'acc_streamline_mode': {'ELA': 4, 'Math': 4},
    'acc_text_to_speech_embed': {'ELA': 4, 'Math': 0},
}

DEMOGRAPHICS_BY_GRADE = {
    1: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'non_binary': 0.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 45.0, 'dmg_eth_pcf': 3.0},
    ),
    2: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'non_binary': 0.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 45.0, 'dmg_eth_pcf': 3.0},
    ),
    3: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'non_binary': 0.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 45.0, 'dmg_eth_pcf': 3.0},
    ),
    4: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 92.0, True: 8.0},
        gender={'female': 48.0, 'male': 50.0, 'non_binary': 0.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 21.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 18.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 47.0, 'dmg_eth_pcf': 2.0},
    ),
    5: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 45.0, True: 55.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 93.0, True: 7.0},
        gender={'female': 49.0, 'male': 51.0, 'non_binary': 0.0, 'not_stated': 0.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 20.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 19.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 47.0, 'dmg_eth_pcf': 2.0},
    ),
    6: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 46.0, True: 54.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 94.0, True: 6.0},
        gender={'female': 49.0, 'male': 49.0, 'non_binary': 1.0, 'not_stated': 1.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 22.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 18.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 46.0, 'dmg_eth_pcf': 2.0},
    ),
    7: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 47.0, True: 53.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 95.0, True: 5.0},
        gender={'female': 48.0, 'male': 50.0, 'non_binary': 1.0, 'not_stated': 1.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 22.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 2.0},
    ),
    8: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 48.0, True: 52.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 95.0, True: 5.0},
        gender={'female': 49.0, 'male': 50.0, 'non_binary': 1.0, 'not_stated': 0.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 21.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 19.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 46.0, 'dmg_eth_pcf': 2.0},
    ),
    9: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 49.0, 'non_binary': 1.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 46.0, 'dmg_eth_pcf': 2.0},
    ),
    10: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 49.0, 'non_binary': 1.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 46.0, 'dmg_eth_pcf': 2.0},
    ),
    11: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 48.0, True: 52.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 95.0, True: 5.0},
        gender={'female': 49.0, 'male': 49.0, 'non_binary': 1.0, 'not_stated': 1.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 21.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 18.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 47.0, 'dmg_eth_pcf': 2.0},
    ),
    12: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 49.0, 'non_binary': 1.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0,
              'dmg_eth_ami': 1.0, 'dmg_eth_wht': 46.0, 'dmg_eth_pcf': 2.0},
    ),
}
LEVELS_BY_GRADE_BY_SUBJ = {
    "Math": {
        1: GradeLevels((14.0, 30.0, 49.0, 7.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(11.30, 29.39, 51.78, 7.53)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(20.0, 38.0, 39.0, 3.0),
                            False: Stats(6.36, 19.82, 61.73, 12.09)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(8.53, 28.76, 54.65, 8.06)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(38.0, 43.0, 19.0, 0.0),
                            False: Stats(11.63, 28.71, 51.97, 7.69)}),
                       gender=DemographicLevels(
                           female=Stats(11.0, 29.0, 52.0, 8.0),
                           male=Stats(16.0, 33.0, 46.0, 5.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                           dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                           dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                           dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0), ), ),
        2: GradeLevels((14.0, 30.0, 49.0, 7.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(11.30, 29.39, 51.78, 7.53)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(20.0, 38.0, 39.0, 3.0),
                            False: Stats(6.36, 19.82, 61.73, 12.09)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(8.53, 28.76, 54.65, 8.06)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(38.0, 43.0, 19.0, 0.0),
                            False: Stats(11.63, 28.71, 51.97, 7.69)}),
                       gender=DemographicLevels(
                           female=Stats(11.0, 29.0, 52.0, 8.0),
                           male=Stats(16.0, 33.0, 46.0, 5.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                           dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                           dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                           dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0), ), ),
        3: GradeLevels((14.0, 30.0, 49.0, 7.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(11.30, 29.39, 51.78, 7.53)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(20.0, 38.0, 39.0, 3.0),
                            False: Stats(6.36, 19.82, 61.73, 12.09)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(8.53, 28.76, 54.65, 8.06)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(38.0, 43.0, 19.0, 0.0),
                            False: Stats(11.63, 28.71, 51.97, 7.69)}),
                       gender=DemographicLevels(
                           female=Stats(11.0, 29.0, 52.0, 8.0),
                           male=Stats(16.0, 33.0, 46.0, 5.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                           dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                           dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                           dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0), ), ),
        4: GradeLevels((9.0, 32.0, 54.0, 5.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(35.0, 45.0, 20.0, 0.0),
                            False: Stats(6.74, 30.87, 56.96, 5.43)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 41.0, 44.0, 2.0),
                            False: Stats(3.91, 20.54, 66.73, 8.82)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(35.0, 45.0, 20.0, 0.0),
                            False: Stats(4.05, 29.52, 60.48, 5.95)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(30.0, 52.0, 18.0, 0.0),
                            False: Stats(7.17, 30.26, 57.13, 5.44)}),
                       gender=DemographicLevels(
                           female=Stats(7.0, 29.0, 58.0, 6.0),
                           male=Stats(12.0, 33.0, 52.0, 3.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(5.0, 28.0, 37.0, 30.0),
                           dmg_eth_ami=Stats(13.0, 39.0, 46.0, 2.0),
                           dmg_eth_asn=Stats(6.0, 20.0, 64.0, 10.0),
                           dmg_eth_blk=Stats(14.0, 43.0, 41.0, 2.0),
                           dmg_eth_hsp=Stats(13.0, 42.0, 43.0, 2.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(6.0, 24.0, 64.0, 6.0), ), ),
        5: GradeLevels((11.0, 31.0, 53.0, 5.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(39.0, 44.0, 17.0, 0.0),
                            False: Stats(8.57, 29.87, 56.13, 5.43)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(15.0, 40.0, 43.0, 2.0),
                            False: Stats(6.11, 20.0, 65.22, 8.67)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(39.0, 44.0, 17.0, 0.0),
                            False: Stats(5.67, 28.52, 59.86, 5.95)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(39.0, 48.0, 13.0, 0.0),
                            False: Stats(8.89, 29.72, 56.01, 5.38)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 30.0, 56.0, 6.0),
                           male=Stats(13.0, 33.0, 51.0, 3.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 29.0, 35.0, 27.0),
                           dmg_eth_ami=Stats(15.0, 42.0, 40.0, 3.0),
                           dmg_eth_asn=Stats(7.0, 20.0, 63.0, 10.0),
                           dmg_eth_blk=Stats(17.0, 43.0, 38.0, 2.0),
                           dmg_eth_hsp=Stats(15.0, 40.0, 43.0, 2.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(7.0, 25.0, 62.0, 6.0), ), ),
        6: GradeLevels((11.0, 33.0, 54.0, 2.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(38.0, 47.0, 15.0, 0.0),
                            False: Stats(8.65, 31.78, 57.39, 2.18)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(16.0, 43.0, 40.0, 1.0),
                            False: Stats(5.13, 21.26, 70.44, 3.17)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(38.0, 47.0, 15.0, 0.0),
                            False: Stats(5.86, 30.33, 61.43, 2.38)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(51.0, 44.0, 5.0, 0.0),
                            False: Stats(8.45, 32.30, 57.13, 2.12)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 58.0, 3.0),
                           male=Stats(13.0, 36.0, 49.0, 2.0),
                           non_binary=Stats(13.0, 36.0, 49.0, 2.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(7.0, 30.0, 32.0, 31.0),
                           dmg_eth_ami=Stats(15.0, 42.0, 40.0, 3.0),
                           dmg_eth_asn=Stats(8.0, 23.0, 64.0, 5.0),
                           dmg_eth_blk=Stats(16.0, 47.0, 36.0, 1.0),
                           dmg_eth_hsp=Stats(17.0, 44.0, 38.0, 1.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(6.0, 26.0, 64.0, 4.0), ), ),
        7: GradeLevels((8.0, 40.0, 48.0, 4.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(33.0, 55.0, 12.0, 0.0),
                            False: Stats(5.83, 38.70, 51.13, 4.34)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 50.0, 36.0, 1.0),
                            False: Stats(2.36, 28.72, 61.53, 7.39)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(33.0, 55.0, 12.0, 0.0),
                            False: Stats(3.24, 37.14, 54.86, 4.76)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(42.0, 54.0, 4.0, 0.0),
                            False: Stats(6.21, 39.26, 50.32, 4.21)}),
                       gender=DemographicLevels(
                           female=Stats(6.0, 36.0, 53.0, 5.0),
                           male=Stats(11.0, 42.0, 44.0, 3.0),
                           non_binary=Stats(11.0, 42.0, 44.0, 3.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(7.0, 28.0, 34.0, 31.0),
                           dmg_eth_ami=Stats(11.0, 50.0, 38.0, 1.0),
                           dmg_eth_asn=Stats(6.0, 26.0, 60.0, 8.0),
                           dmg_eth_blk=Stats(13.0, 53.0, 33.0, 1.0),
                           dmg_eth_hsp=Stats(13.0, 51.0, 35.0, 1.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.0, 31.0, 59.0, 5.0), ), ),
        8: GradeLevels((7.0, 43.0, 48.0, 2.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 60.0, 11.0, 0.0),
                            False: Stats(5.09, 41.52, 51.22, 2.17)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(11.0, 54.0, 34.0, 1.0),
                            False: Stats(2.67, 31.08, 63.17, 3.08)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 60.0, 11.0, 0.0),
                            False: Stats(2.81, 39.76, 55.05, 2.38)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(43.0, 54.0, 3.0, 0.0),
                            False: Stats(5.11, 42.42, 50.37, 2.10)}),
                       gender=DemographicLevels(
                           female=Stats(5.0, 39.0, 53.0, 3.0),
                           male=Stats(9.0, 46.0, 44.0, 1.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(8.0, 30.0, 42.0, 20.0),
                           dmg_eth_ami=Stats(10.0, 52.0, 37.0, 1.0),
                           dmg_eth_asn=Stats(7.0, 28.0, 61.0, 4.0),
                           dmg_eth_blk=Stats(11.0, 59.0, 30.0, 0.0),
                           dmg_eth_hsp=Stats(12.0, 55.0, 33.0, 0.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(4.0, 33.0, 60.0, 3.0), ), ),
        9: GradeLevels((14.0, 30.0, 49.0, 7.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(11.30, 29.39, 51.78, 7.53)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(20.0, 38.0, 39.0, 3.0),
                            False: Stats(6.36, 19.82, 61.73, 12.09)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(8.53, 28.76, 54.65, 8.06)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(38.0, 43.0, 19.0, 0.0),
                            False: Stats(11.63, 28.71, 51.97, 7.69)}),
                       gender=DemographicLevels(
                           female=Stats(11.0, 29.0, 52.0, 8.0),
                           male=Stats(16.0, 33.0, 46.0, 5.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                           dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                           dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                           dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0), ), ),
        10: GradeLevels((14.0, 30.0, 49.0, 7.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(45.0, 37.0, 17.0, 1.0),
                             False: Stats(11.30, 29.39, 51.78, 7.53)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(20.0, 38.0, 39.0, 3.0),
                             False: Stats(6.36, 19.82, 61.73, 12.09)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(45.0, 37.0, 17.0, 1.0),
                             False: Stats(8.53, 28.76, 54.65, 8.06)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(38.0, 43.0, 19.0, 0.0),
                             False: Stats(11.63, 28.71, 51.97, 7.69)}),
                        gender=DemographicLevels(
                            female=Stats(11.0, 29.0, 52.0, 8.0),
                            male=Stats(16.0, 33.0, 46.0, 5.0),
                            non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                            dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                            dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                            dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0), ), ),
        11: GradeLevels((7.0, 43.0, 48.0, 2.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(29.0, 60.0, 11.0, 0.0),
                             False: Stats(5.09, 41.52, 51.22, 2.17)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(11.0, 54.0, 34.0, 1.0),
                             False: Stats(2.67, 31.08, 63.17, 3.08)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(29.0, 60.0, 11.0, 0.0),
                             False: Stats(2.81, 39.76, 55.05, 2.38)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(43.0, 54.0, 3.0, 0.0),
                             False: Stats(5.11, 42.42, 50.37, 2.10)}),
                        gender=DemographicLevels(
                            female=Stats(5.0, 39.0, 53.0, 3.0),
                            male=Stats(9.0, 46.0, 44.0, 1.0),
                            non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(10.0, 52.0, 37.0, 1.0),
                            dmg_eth_asn=Stats(7.0, 28.0, 61.0, 4.0),
                            dmg_eth_blk=Stats(11.0, 59.0, 30.0, 0.0),
                            dmg_eth_hsp=Stats(12.0, 55.0, 33.0, 0.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                            dmg_eth_wht=Stats(4.0, 33.0, 60.0, 3.0), ), ),
        12: GradeLevels((14.0, 30.0, 49.0, 7.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(45.0, 37.0, 17.0, 1.0),
                             False: Stats(11.30, 29.39, 51.78, 7.51)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(20.0, 38.0, 39.0, 3.0),
                             False: Stats(6.36, 19.82, 61.73, 12.09)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(45.0, 37.0, 17.0, 1.0),
                             False: Stats(8.53, 28.76, 54.65, 8.06)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(38.0, 43.0, 19.0, 0.0),
                             False: Stats(11.63, 28.71, 51.97, 7.69)}),
                        gender=DemographicLevels(
                            female=Stats(11.0, 29.0, 52.0, 8.0),
                            male=Stats(16.0, 33.0, 46.0, 5.0),
                            non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                            dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                            dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                            dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0), ), ),
    },
    "ELA": {
        1: GradeLevels((9.0, 30.0, 48.0, 13.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(7.49, 29.10, 49.66, 13.75)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 37.0, 42.0, 8.0),
                            False: Stats(3.70, 20.72, 55.95, 19.63)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(5.47, 27.88, 51.88, 14.77)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(23.0, 42.0, 32.0, 3.0),
                            False: Stats(7.62, 28.81, 49.58, 13.99)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 49.0, 12.0),
                           male=Stats(10.0, 29.0, 47.0, 14.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                           dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                           dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                           dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4), ), ),
        2: GradeLevels((9.0, 30.0, 48.0, 13.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(7.49, 29.10, 49.66, 13.75)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 37.0, 42.0, 8.0),
                            False: Stats(3.70, 20.72, 55.95, 19.63)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(5.47, 27.88, 51.88, 14.77)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(23.0, 42.0, 32.0, 3.0),
                            False: Stats(7.62, 28.81, 49.58, 13.99)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 49.0, 12.0),
                           male=Stats(10.0, 29.0, 47.0, 14.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                           dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                           dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                           dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4), ), ),
        3: GradeLevels((9.0, 30.0, 48.0, 13.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(7.49, 29.10, 49.66, 13.75)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 37.0, 42.0, 8.0),
                            False: Stats(3.70, 20.72, 55.95, 19.63)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(5.47, 27.88, 51.88, 14.77)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(23.0, 42.0, 32.0, 3.0),
                            False: Stats(7.62, 28.81, 49.58, 13.99)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 49.0, 12.0),
                           male=Stats(10.0, 29.0, 47.0, 14.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                           dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                           dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                           dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4), ), ),
        4: GradeLevels((5.0, 26.0, 39.0, 30.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(21.0, 44.0, 26.0, 9.0),
                            False: Stats(3.61, 24.43, 40.13, 31.83)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(8.0, 33.0, 38.0, 21.0),
                            False: Stats(1.18, 17.09, 40.27, 41.46)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(21.0, 44.0, 26.0, 9.0),
                            False: Stats(1.95, 22.57, 41.48, 34.0)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(15.0, 42.0, 33.0, 10.0),
                            False: Stats(4.01, 24.42, 39.59, 31.98)}),
                       gender=DemographicLevels(
                           female=Stats(5.0, 26.0, 39.0, 30.0),
                           male=Stats(5.0, 26.0, 39.0, 30.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(5.0, 28.0, 37.0, 30.0),
                           dmg_eth_ami=Stats(8.0, 34.0, 36.0, 22.0),
                           dmg_eth_asn=Stats(2.0, 10.0, 31.0, 57.0),
                           dmg_eth_blk=Stats(8.0, 40.0, 37.0, 15.0),
                           dmg_eth_hsp=Stats(8.0, 33.0, 40.0, 19.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(3.0, 19.0, 40.4468, 37.5532), ), ),
        5: GradeLevels((7.0, 26.0, 39.0, 28.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(27.0, 42.0, 25.0, 6.0),
                            False: Stats(5.26, 24.61, 40.22, 29.91)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(10.0, 33.0, 37.0, 20.0),
                            False: Stats(3.18, 17.09, 41.55, 38.18)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(27.0, 42.0, 25.0, 6.0),
                            False: Stats(3.19, 22.95, 41.67, 32.19)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(21.0, 42.0, 28.0, 9.0),
                            False: Stats(5.78, 24.61, 39.96, 29.65)}),
                       gender=DemographicLevels(
                           female=Stats(7.0, 25.0, 40.0, 28.0),
                           male=Stats(7.1, 26.9, 37.64, 28.36),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 29.0, 35.0, 27.0),
                           dmg_eth_ami=Stats(13.0, 34.0, 35.0, 18.0),
                           dmg_eth_asn=Stats(3.0, 11.0, 30.0, 56.0),
                           dmg_eth_blk=Stats(13.0, 36.0, 36.0, 15.0),
                           dmg_eth_hsp=Stats(10.0, 33.0, 38.0, 19.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(4.85, 21.15, 41.42, 32.58), ), ),
        6: GradeLevels((8.0, 27.0, 34.0, 31.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 44.0, 21.0, 6.0),
                            False: Stats(6.17, 25.53, 35.13, 33.17)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(12.0, 35.0, 33.0, 20.0),
                            False: Stats(3.30, 17.61, 35.17, 43.92)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 44.0, 21.0, 6.0),
                            False: Stats(4.0, 23.76, 36.48, 35.76)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(27.0, 44.0, 21.0, 8.0),
                            False: Stats(6.79, 25.91, 34.83, 32.47)}),
                       gender=DemographicLevels(
                           female=Stats(7.0, 26.0, 34.67, 32.33),
                           male=Stats(9.0, 28.0, 33.0, 30.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(7.0, 30.0, 32.0, 31.0),
                           dmg_eth_ami=Stats(12.0, 35.0, 34.0, 19.0),
                           dmg_eth_asn=Stats(3.0, 11.0, 26.0, 60.0),
                           dmg_eth_blk=Stats(14.68, 38.32, 32.0, 15.0),
                           dmg_eth_hsp=Stats(12.0, 36.0, 34.0, 18.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.0, 21.26, 35.70, 38.04), ), ),
        7: GradeLevels((9.0, 26.0, 34.0, 31.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(31.0, 43.0, 21.0, 5.0),
                            False: Stats(7.09, 24.52, 35.13, 33.26)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 35.0, 33.0, 19.0),
                            False: Stats(4.49, 15.85, 35.13, 44.53)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(31.0, 43.0, 21.0, 5.0),
                            False: Stats(4.81, 22.76, 36.48, 35.95)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(30.0, 43.0, 20.0, 7.0),
                            False: Stats(7.66, 24.92, 34.89, 32.53)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 26.0, 35.0, 31.0),
                           male=Stats(10.0, 26.0, 32.73, 31.27),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(7.0, 28.0, 34.0, 31.0),
                           dmg_eth_ami=Stats(10.0, 35.0, 34.0, 21.0),
                           dmg_eth_asn=Stats(3.0, 12.0, 25.0, 60.0),
                           dmg_eth_blk=Stats(18.3684, 37.6316, 31.0, 13.0),
                           dmg_eth_hsp=Stats(13.0, 36.0, 34.0, 17.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.0, 19.0, 36.4167, 39.5833), ), ),
        8: GradeLevels((7.0, 32.0, 41.0, 20.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(27.0, 50.0, 21.0, 2.0),
                            False: Stats(5.26, 30.43, 42.74, 21.57)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(11.0, 40.0, 37.0, 12.0),
                            False: Stats(2.67, 23.33, 45.33, 28.67)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(27.0, 50.0, 21.0, 2.0),
                            False: Stats(3.19, 28.57, 44.81, 23.43)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(22.0, 45.0, 27.0, 6.0),
                            False: Stats(6.05, 31.17, 41.89, 20.89)}),
                       gender=DemographicLevels(
                           female=Stats(6.0, 31.0, 41.82, 21.18),
                           male=Stats(8.0, 33.0, 40.0, 19.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(8.0, 30.0, 42.0, 20.0),
                           dmg_eth_ami=Stats(9.0, 40.0, 39.0, 12.0),
                           dmg_eth_asn=Stats(2.0, 14.0, 37.0, 47.0),
                           dmg_eth_blk=Stats(13.5, 45.5, 34.0, 7.0),
                           dmg_eth_hsp=Stats(11.0, 40.0, 39.0, 10.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(4.0, 26.56, 45.06, 24.38), ), ),
        9: GradeLevels((9.0, 30.0, 48.0, 13.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(7.49, 29.10, 49.66, 13.75)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 37.0, 42.0, 8.0),
                            False: Stats(3.70, 20.72, 55.95, 19.63)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(5.47, 27.88, 51.88, 14.77)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(23.0, 42.0, 32.0, 3.0),
                            False: Stats(7.62, 28.81, 49.58, 13.99)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 49.0, 12.0),
                           male=Stats(10.0, 29.0, 47.0, 14.0),
                           non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                           dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                           dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                           dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4), ), ),
        10: GradeLevels((9.0, 30.0, 48.0, 13.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(29.0, 42.0, 26.0, 3.0),
                             False: Stats(7.49, 29.10, 49.66, 13.75)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(13.0, 37.0, 42.0, 8.0),
                             False: Stats(3.70, 20.72, 55.95, 19.63)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(29.0, 42.0, 26.0, 3.0),
                             False: Stats(5.47, 27.88, 51.88, 14.77)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(23.0, 42.0, 32.0, 3.0),
                             False: Stats(7.62, 28.81, 49.58, 13.99)}),
                        gender=DemographicLevels(
                            female=Stats(8.0, 31.0, 49.0, 12.0),
                            male=Stats(10.0, 29.0, 47.0, 14.0),
                            non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                            dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                            dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                            dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                            dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4), ), ),
        11: GradeLevels((7.0, 32.0, 41.0, 20.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(27.0, 50.0, 21.0, 2.0),
                             False: Stats(5.26, 30.43, 42.74, 21.57)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(11.0, 40.0, 37.0, 12.0),
                             False: Stats(2.67, 23.33, 45.33, 28.67)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(27.0, 50.0, 21.0, 2.0),
                             False: Stats(3.19, 28.57, 44.81, 23.43)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(22.0, 45.0, 27.0, 6.0),
                             False: Stats(6.05, 31.17, 41.89, 20.89)}),
                        gender=DemographicLevels(
                            female=Stats(6.0, 31.0, 43.0, 20.0),
                            male=Stats(8.0, 33.0, 38.76, 20.24),
                            non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(9.0, 40.0, 39.0, 12.0),
                            dmg_eth_asn=Stats(2.0, 14.0, 37.0, 47.0),
                            dmg_eth_blk=Stats(12.95, 46.05, 34.0, 7.0),
                            dmg_eth_hsp=Stats(11.0, 40.0, 39.0, 10.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                            dmg_eth_wht=Stats(4.0, 25.92, 45.19, 24.89), ), ),
        12: GradeLevels((9.0, 30.0, 48.0, 13.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(29.0, 42.0, 26.0, 3.0),
                             False: Stats(7.49, 29.10, 49.66, 13.75)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(13.0, 37.0, 42.0, 8.0),
                             False: Stats(3.70, 20.72, 55.95, 19.63)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(29.0, 42.0, 26.0, 3.0),
                             False: Stats(5.47, 27.88, 51.88, 14.77)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(23.0, 42.0, 32.0, 3.0),
                             False: Stats(7.62, 28.81, 49.58, 13.99)}),
                        gender=DemographicLevels(
                            female=Stats(8.0, 31.0, 49.0, 12.0),
                            male=Stats(10.0, 29.0, 47.0, 14.0),
                            non_binary=Stats(9.0, 30.0, 51.0, 10.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0), ),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                            dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                            dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                            dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                            dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4), ), ),
    },
}

# BEGIN interim assessment configuration ##

# % of students that have might take at least 1 interim assessment block
IAB_STUDENT_RATE = 0.90

# In the following, the year is the year adjustment (offset of the year from the start of the schoolyear)
# However, python (perhaps reasonably) doesn't do a year 0, so we'll need to subtract 1 from these later
IAB_EFFECTIVE_DATES = (datetime.date(1, 10, 1),
                       datetime.date(2, 1, 1),
                       datetime.date(2, 3, 1),)

# subject → grade → block name
IAB_NAMES = {'ELA': {3: ('Read Literary Texts',
                         'Read Informational Texts',
                         'Edit/Revise',
                         'Brief Writes',
                         'Listen/Interpret',
                         'Research',
                         'Narrative Performance Task',
                         'Informational Performance Task',
                         'Opinion Performance Task'),
                     4: ('Read Literary Texts',
                         'Read Informational Texts',
                         'Edit/Revise',
                         'Brief Writes',
                         'Listen/Interpret',
                         'Research',
                         'Narrative Performance Task',
                         'Informational Performance Task',
                         'Opinion Performance Task'),
                     5: ('Read Literary Texts',
                         'Read Informational Texts',
                         'Edit/Revise',
                         'Brief Writes',
                         'Listen/Interpret',
                         'Research',
                         'Narrative Performance Task',
                         'Informational Performance Task',
                         'Opinion Performance Task'),
                     6: ('Read Literary Texts',
                         'Read Informational Texts',
                         'Edit/Revise',
                         'Brief Writes',
                         'Listen/Interpret',
                         'Research',
                         'Narrative Performance Task',
                         'Explanatory Performance Task',
                         'Argument Performance Task'),
                     7: ('Read Literary Texts',
                         'Read Informational Texts',
                         'Edit/Revise',
                         'Brief Writes',
                         'Listen/Interpret',
                         'Research',
                         'Narrative Performance Task',
                         'Explanatory Performance Task',
                         'Argument Performance Task'),
                     8: ('Read Literary Texts',
                         'Read Informational Texts',
                         'Edit/Revise',
                         'Brief Writes',
                         'Listen/Interpret',
                         'Research',
                         'Narrative Performance Task',
                         'Explanatory Performance Task',
                         'Argument Performance Task'),
                     11: ('Read Literary Texts',
                          'Read Informational Texts',
                          'Edit/Revise',
                          'Brief Writes',
                          'Listen/Interpret',
                          'Research',
                          'Narrative Performance Task',
                          'Explanatory Performance Task',
                          'Argument Performance Task'),},
             'Math': {3: ('Operations and Algebraic Thinking',
                          'Numbers and Operations in Base 10',
                          'Fractions',
                          'Measurement and Data',
                          'Mathematics Performance Task'),
                      4: ('Operations and Algebraic Thinking',
                          'Numbers and Operations in Base 10',
                          'Fractions',
                          'Geometry',
                          'Measurement and Data',
                          'Mathematics Performance Task'),
                      5: ('Operations and Algebraic Thinking',
                          'Numbers and Operations in Base 10',
                          'Fractions',
                          'Geometry',
                          'Measurement and Data',
                          'Mathematics Performance Task'),
                      6: ('Ratio and Proportional Relationships',
                          'Number System',
                          'Expressions and Equations',
                          'Geometry',
                          'Statistics and Probability',
                          'Mathematics Performance Task'),
                      7: ('Ratio and Proportional Relationships',
                          'Number System',
                          'Expressions and Equations',
                          'Geometry',
                          'Statistics and Probability',
                          'Mathematics Performance Task'),
                      8: ('Expressions & Equations I (and Proportionality)',
                          'Expressions & Equations II',
                          'Functions',
                          'Geometry',
                          'Mathematics Performance Task'),
                      11: ('Algebra and Functions - Linear Functions',
                           'Algebra and Functions - Quadratic Functions',
                           'Algebra and Functions - Exponential Functions',
                           'Algebra and Functions - Polynomials',
                           'Algebra and Functions - Radicals',
                           'Algebra and Functions - Rational Functions',
                           'Algebra and Functions - Trigonometric Functions',
                           'Geometry - Transformations in Geometry',
                           'Geometry - Right Triangle Ratios in Geometry',
                           'Geometry - Three - Dimensional Geometry',
                           'Geometry - Proofs',
                           'Geometry - Circles',
                           'Geometry - Applications',
                           'Interpreting Categorical and Quantitative Data',
                           'Probability',
                           'Making Inferences and Justifying Conclusions',
                           'Mathematics Performance Task')}}

# END interim assessment configuration ##
