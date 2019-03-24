"""
Unit tests for the assessment module.

"""

import datetime
from random import choice, sample, random
from string import ascii_uppercase

from pytest import raises

import datagen.config.cfg as cfg
import datagen.generators.hierarchy as hier_gen
import datagen.generators.population as pop_gen
import datagen.generators.summative_or_ica_assessment as asmt_gen
import datagen.model.itemdata as item_lvl_data
from datagen.generators.assessment import generate_response, _pick_accommodation_code
from datagen.model.assessment import Assessment
from datagen.model.item import AssessmentItem
from datagen.model.scorable import Scorable
from datagen.model.segment import AssessmentSegment
from datagen.util.id_gen import IDGen

ID_GEN = IDGen()

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


def test_generate_item_data():
    item_data = item_lvl_data.AssessmentOutcomeItemData()
    item_data.key = 1938
    item_data.segment_id = '(SBAC)SBAC-MG110PT-S2-ELA-7-Spring-2014-2015'
    item_data.position = 19
    item_data.format = 'MC'

    assert item_data.key == 1938
    assert item_data.segment_id == '(SBAC)SBAC-MG110PT-S2-ELA-7-Spring-2014-2015'
    assert item_data.position == 19
    assert item_data.format == 'MC'


def test_generate_assessment_outcome_default_status():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    asmt_out = asmt_gen.generate_assessment_outcome(datetime.date(2015, 5, 15), student, asmt, ID_GEN)

    # Test
    assert asmt_out.result_status == 'C'


def test_generate_assessment_outcome_scores():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    asmt_out = asmt_gen.generate_assessment_outcome(datetime.date(2015, 5, 15), student, asmt, ID_GEN)

    # Tests
    assert 2114 <= asmt_out.overall.score <= 2623
    assert 2114 <= asmt_out.claim_1_score <= 2623
    assert 2114 <= asmt_out.claim_2_score <= 2623
    assert 2114 <= asmt_out.claim_3_score <= 2623


def test_generate_assessment_outcome_summative_taken_date():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'Math', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    asmt_out = asmt_gen.generate_assessment_outcome(datetime.date(2015, 5, 15), student, asmt, ID_GEN)

    # Test
    assert asmt_out.date_taken == datetime.date(2015, 5, 15)


def test_generate_assessment_outcome_interim_taken_date():
    # Create objects
    asmt = generate_assessment('INTERIM COMPREHENSIVE', 2015, 'Math', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    asmt_out = asmt_gen.generate_assessment_outcome(datetime.date(2015, 5, 15), student, asmt, ID_GEN)

    # Test
    assert asmt_out.date_taken == datetime.date(2015, 5, 15)


def test_generate_assessment_outcome_accommodations_ela():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    asmt_out = asmt_gen.generate_assessment_outcome(datetime.date(2015, 5, 15), student, asmt, ID_GEN)

    # Tests
    assert 4 <= asmt_out.acc_asl_video_embed <= 26
    assert 4 <= asmt_out.acc_print_on_demand_items_nonembed <= 26
    assert 4 <= asmt_out.acc_noise_buffer_nonembed <= 26
    assert 4 <= asmt_out.acc_braile_embed <= 26
    assert 4 <= asmt_out.acc_closed_captioning_embed <= 26
    assert 4 <= asmt_out.acc_text_to_speech_embed <= 26
    assert asmt_out.acc_abacus_nonembed == 0
    assert 4 <= asmt_out.acc_alternate_response_options_nonembed <= 26
    assert asmt_out.acc_calculator_nonembed == 0
    assert asmt_out.acc_multiplication_table_nonembed == 0
    assert 4 <= asmt_out.acc_alternate_response_options_nonembed <= 26
    assert 4 <= asmt_out.acc_read_aloud_nonembed <= 26
    assert 4 <= asmt_out.acc_scribe_nonembed <= 26
    assert 4 <= asmt_out.acc_speech_to_text_nonembed <= 26
    assert 4 <= asmt_out.acc_streamline_mode <= 26


def test_generate_assessment_outcome_accommodations_math():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'Math', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    asmt_out = asmt_gen.generate_assessment_outcome(datetime.date(2015, 5, 15), student, asmt, ID_GEN)

    # Tests
    assert 4 <= asmt_out.acc_asl_video_embed <= 26
    assert 4 <= asmt_out.acc_print_on_demand_items_nonembed <= 26
    assert 4 <= asmt_out.acc_noise_buffer_nonembed <= 26
    assert 4 <= asmt_out.acc_braile_embed <= 26
    assert asmt_out.acc_closed_captioning_embed == 0
    assert asmt_out.acc_text_to_speech_embed == 0
    assert 4 <= asmt_out.acc_abacus_nonembed <= 26
    assert 4 <= asmt_out.acc_alternate_response_options_nonembed <= 26
    assert 4 <= asmt_out.acc_calculator_nonembed <= 26
    assert 4 <= asmt_out.acc_multiplication_table_nonembed <= 26
    assert 4 <= asmt_out.acc_alternate_response_options_nonembed <= 26
    assert asmt_out.acc_read_aloud_nonembed == 0
    assert asmt_out.acc_scribe_nonembed == 0
    assert asmt_out.acc_speech_to_text_nonembed == 0
    assert 4 <= asmt_out.acc_streamline_mode <= 26


def test_pick_default_accommodation_code_negative():
    with raises(ValueError):
        _pick_accommodation_code(-1)


def test_pick_default_accommodation_code_too_big():
    with raises(ValueError):
        _pick_accommodation_code(5)


def test_pick_default_accommodation_code_0():
    code = _pick_accommodation_code(0)
    assert code == 0


def test_pick_default_accommodation_code_four():
    assert 4 <= _pick_accommodation_code(4) <= 26


def test_create_assessment_outcome_object_item_data():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    asmt_gen.create_assessment_outcome_object(datetime.date(2015, 5, 15), student, asmt, ID_GEN, outcomes,
                                              skip_rate=0, retake_rate=0, delete_rate=0, update_rate=0, gen_item=True)

    # Tests
    assert len(outcomes) == 1
    assert len(outcomes[asmt.guid][0].item_data) == cfg.ASMT_ITEM_BANK_SIZE


def test_create_assessment_outcome_object_skipped():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    asmt_gen.create_assessment_outcome_object(datetime.date(2015, 5, 15), student, asmt, ID_GEN, outcomes,
                                              skip_rate=1, retake_rate=0, delete_rate=0, update_rate=0, gen_item=False)

    # Tests
    assert len(outcomes) == 0


def test_create_assessment_outcome_object_one_active_result():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    asmt_gen.create_assessment_outcome_object(datetime.date(2015, 5, 15), student, asmt, ID_GEN, outcomes,
                                              skip_rate=0, retake_rate=0, delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid][0].result_status == 'C'
    assert outcomes[asmt.guid][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_object_retake_results():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    asmt_gen.create_assessment_outcome_object(datetime.date(2015, 5, 15), student, asmt, ID_GEN, outcomes,
                                              skip_rate=0, retake_rate=1, delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid][0].result_status == 'I'
    assert outcomes[asmt.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt.guid][1].result_status == 'C'
    assert outcomes[asmt.guid][1].date_taken == datetime.date(2015, 5, 22)


def test_create_assessment_outcome_object_one_deleted_result():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    asmt_gen.create_assessment_outcome_object(datetime.date(2015, 5, 15), student, asmt, ID_GEN, outcomes,
                                              skip_rate=0, retake_rate=0, delete_rate=1, update_rate=0)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid][0].result_status == 'D'
    assert outcomes[asmt.guid][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_object_update_no_second_delete_results():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    asmt_gen.create_assessment_outcome_object(datetime.date(2015, 5, 15), student, asmt, ID_GEN, outcomes,
                                              skip_rate=0, retake_rate=0, delete_rate=0, update_rate=1)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid][0].result_status == 'D'
    assert outcomes[asmt.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt.guid][1].result_status == 'C'
    assert outcomes[asmt.guid][1].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_object_update_second_delete_results():
    # Create objects
    asmt = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    asmt_gen.create_assessment_outcome_object(datetime.date(2015, 5, 15), student, asmt, ID_GEN, outcomes,
                                              skip_rate=0, retake_rate=0, delete_rate=1, update_rate=1)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid][0].result_status == 'D'
    assert outcomes[asmt.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt.guid][1].result_status == 'D'
    assert outcomes[asmt.guid][1].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_no_interims_skipped():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, [], ID_GEN, outcomes, skip_rate=1, retake_rate=0,
                                        delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 0


def test_create_assessment_outcome_objects_no_interims_one_active_result():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, [], ID_GEN, outcomes, skip_rate=0, retake_rate=0,
                                        delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid][0].result_status == 'C'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_no_interims_retake_results():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, [], ID_GEN, outcomes, skip_rate=0, retake_rate=1,
                                        delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid][0].result_status == 'I'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid][1].result_status == 'C'
    assert outcomes[asmt_summ.guid][1].date_taken == datetime.date(2015, 5, 22)


def test_create_assessment_outcome_objects_no_interim_one_deleted_result():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, [], ID_GEN, outcomes, skip_rate=0, retake_rate=0,
                                        delete_rate=1, update_rate=0)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid][0].result_status == 'D'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_no_interim_update_no_second_delete_results():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, [], ID_GEN, outcomes, skip_rate=0, retake_rate=0,
                                        delete_rate=0, update_rate=1)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid][0].result_status == 'D'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid][1].result_status == 'C'
    assert outcomes[asmt_summ.guid][1].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_no_interim_update_second_delete_results():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, [], ID_GEN, outcomes, skip_rate=0, retake_rate=0,
                                        delete_rate=1, update_rate=1)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid][0].result_status == 'D'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid][1].result_status == 'D'
    assert outcomes[asmt_summ.guid][1].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_interims_skipped():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    interim_asmts = [generate_assessment('INTERIM COMPREHENSIVE', 2015, 'ELA', 3, ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, interim_asmts, ID_GEN, outcomes,
                                        skip_rate=1, retake_rate=0, delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 0


def test_create_assessment_outcome_objects_interims_one_active_result():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    interim_asmts = [generate_assessment('INTERIM COMPREHENSIVE', 2015, 'ELA', 3, ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, interim_asmts, ID_GEN, outcomes,
                                        skip_rate=0, retake_rate=0, delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 2
    assert outcomes[asmt_summ.guid][0].assessment.type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid][0].result_status == 'C'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid][0].assessment.type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid][0].result_status == 'C'
    assert outcomes[interim_asmts[0].guid][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_interims_retake_results():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    interim_asmts = [generate_assessment('INTERIM COMPREHENSIVE', 2015, 'ELA', 3, ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, interim_asmts, ID_GEN, outcomes,
                                        skip_rate=0, retake_rate=1, delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 2
    assert outcomes[asmt_summ.guid][0].assessment.type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid][0].result_status == 'I'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid][1].assessment.type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid][1].result_status == 'C'
    assert outcomes[asmt_summ.guid][1].date_taken == datetime.date(2015, 5, 22)
    assert outcomes[interim_asmts[0].guid][0].assessment.type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid][0].result_status == 'I'
    assert outcomes[interim_asmts[0].guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid][1].assessment.type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid][1].result_status == 'C'
    assert outcomes[interim_asmts[0].guid][1].date_taken == datetime.date(2015, 5, 22)


def test_create_assessment_outcome_objects_interim_one_deleted_result():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    interim_asmts = [generate_assessment('INTERIM COMPREHENSIVE', 2015, 'ELA', 3, ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, interim_asmts, ID_GEN, outcomes,
                                        skip_rate=0, retake_rate=0, delete_rate=1, update_rate=0)

    # Tests
    assert len(outcomes) == 2
    assert outcomes[asmt_summ.guid][0].assessment.type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid][0].result_status == 'D'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid][0].assessment.type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid][0].result_status == 'D'
    assert outcomes[interim_asmts[0].guid][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_interim_update_no_second_delete_results():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    interim_asmts = [generate_assessment('INTERIM COMPREHENSIVE', 2015, 'ELA', 3, ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, interim_asmts, ID_GEN, outcomes,
                                        skip_rate=0, retake_rate=0, delete_rate=0, update_rate=1)

    # Tests
    assert len(outcomes) == 2
    assert outcomes[asmt_summ.guid][0].assessment.type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid][0].result_status == 'D'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid][1].assessment.type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid][1].result_status == 'C'
    assert outcomes[asmt_summ.guid][1].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid][0].assessment.type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid][0].result_status == 'D'
    assert outcomes[interim_asmts[0].guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid][1].assessment.type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid][1].result_status == 'C'
    assert outcomes[interim_asmts[0].guid][1].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_interim_update_second_delete_results():
    # Create objects
    asmt_summ = generate_assessment('SUMMATIVE', 2015, 'ELA', 3, ID_GEN)
    interim_asmts = [generate_assessment('INTERIM COMPREHENSIVE', 2015, 'ELA', 3, ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    outcomes = {}

    # Create outcomes
    __create_assessment_outcome_objects(student, asmt_summ, interim_asmts, ID_GEN, outcomes,
                                        skip_rate=0, retake_rate=0, delete_rate=1, update_rate=1)

    # Tests
    assert len(outcomes) == 2
    assert outcomes[asmt_summ.guid][0].assessment.type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid][0].result_status == 'D'
    assert outcomes[asmt_summ.guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid][1].assessment.type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid][1].result_status == 'D'
    assert outcomes[asmt_summ.guid][1].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid][0].assessment.type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid][0].result_status == 'D'
    assert outcomes[interim_asmts[0].guid][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid][1].assessment.type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid][1].result_status == 'D'
    assert outcomes[interim_asmts[0].guid][1].date_taken == datetime.date(2015, 5, 15)


def test_generate_response_for_mc():
    item = AssessmentItem()
    item.type = 'MC'
    item.options_count = 4
    item.answer_key = 'B'
    item.max_score = 1
    item.difficulty = 2

    aid = item_lvl_data.AssessmentOutcomeItemData()
    generate_response(aid, item)

    assert aid.is_selected == '1'
    assert aid.page_time > 0
    if aid.score == 0:
        assert aid.response_value != 'B'
    else:
        assert aid.score == 1
        assert aid.response_value == 'B'


def test_generate_response_for_ms():
    item = AssessmentItem()
    item.type = 'MS'
    item.options_count = 6
    item.answer_key = 'B,F'
    item.max_score = 2
    item.difficulty = 2

    for _ in range(0, 100):
        aid = item_lvl_data.AssessmentOutcomeItemData()
        generate_response(aid, item)

        assert aid.is_selected == '1'
        assert aid.page_time > 0
        if aid.score == 0:
            assert 'B' not in aid.response_value
        else:
            assert aid.score == 2
            assert aid.response_value == 'B,F'


def test_generate_response_for_sa():
    item = AssessmentItem()
    item.type = 'SA'
    item.max_score = 2
    item.difficulty = 2

    for _ in range(0, 100):
        aid = item_lvl_data.AssessmentOutcomeItemData()
        generate_response(aid, item)

        assert aid.is_selected == '1'
        assert aid.page_time > 1000
        assert len(aid.response_value) > 40
        assert aid.score in (0, 2)


def test_generate_response_for_wer():
    item = AssessmentItem()
    item.type = 'WER'
    item.max_score = 6
    item.difficulty = 2

    for _ in range(0, 100):
        aid = item_lvl_data.AssessmentOutcomeItemData()
        generate_response(aid, item)

        assert aid.is_selected == '1'
        assert aid.page_time > 1000
        assert len(aid.response_value) > 80
        assert aid.score in (0, 1, 2, 3, 4, 5, 6)
        assert len(aid.sub_scores) == 3


def test_generate_response_for_other():
    item = AssessmentItem()
    item.type = 'EQ'
    item.max_score = 1
    item.difficulty = 2

    aid = item_lvl_data.AssessmentOutcomeItemData()
    generate_response(aid, item)

    assert aid.is_selected == '1'
    assert aid.page_time > 1000
    if aid.score == 0:
        assert 'good' not in aid.response_value
    else:
        assert aid.score == 1
        assert 'good' in aid.response_value


def test_generate_response_low_capability():
    item = AssessmentItem()
    item.type = 'EQ'
    item.max_score = 1
    item.difficulty = 2

    total = 0
    for _ in range(0, 100):
        aid = item_lvl_data.AssessmentOutcomeItemData()
        generate_response(aid, item, 0.0)
        total += aid.score
    assert total < 50


def test_generate_response_high_capability():
    item = AssessmentItem()
    item.type = 'EQ'
    item.max_score = 1
    item.difficulty = 2

    total = 0
    for _ in range(0, 100):
        aid = item_lvl_data.AssessmentOutcomeItemData()
        generate_response(aid, item, 4.0)
        total += aid.score
    assert total > 50


# Helper to replace removed method
def __create_assessment_outcome_objects(student, asmt_summ, interim_asmts, id_gen, assessment_results, skip_rate,
                                        retake_rate, delete_rate, update_rate):
    # Create the summative assessment outcome
    asmt_gen.create_assessment_outcome_object(datetime.date(2015, 5, 15), student, asmt_summ, id_gen,
                                              assessment_results, skip_rate, retake_rate, delete_rate,
                                              update_rate, False)

    # Generate interim assessment results (list will be empty if school does not perform
    # interim assessments)
    for asmt in interim_asmts:
        # Create the interim assessment outcome
        asmt_gen.create_assessment_outcome_object(datetime.date(2015, 5, 15), student, asmt, id_gen,
                                                  assessment_results, skip_rate, retake_rate, delete_rate,
                                                  update_rate, False)


def generate_assessment(asmt_type, asmt_year, subject, grade, id_gen, from_date=None, to_date=None,
                        claim_definitions=cfg.CLAIM_DEFINITIONS, gen_item=True):
    """
    The datagen module used to have the ability to generate assessments. That is no longer available
    (the assessment packages are loaded from tabulator output) so we need a helper method that can
    be used to generate a test assessment object used to generate assessment outcomes.
    
    @param asmt_type: Assessment asmt_type
    @param asmt_year: Assessment year
    @param subject: Assessment subject
    @param grade: Assessment grade
    @param id_gen: ID generator
    @param from_date: Assessment from date
    @param to_date: Assessment to date
    @param claim_definitions: Definitions for claims to generate
    @param gen_item: If should create item-level item bank
    @returns: The assessment object
    """
    # Get the claim definitions for this subject
    if subject not in claim_definitions:
        raise KeyError("Subject '{}' not found in claim definitions".format(subject))

    claims = claim_definitions[subject]
    asmt_scale_scores = ASMT_SCALE_SCORE[subject][grade]

    sa = Assessment() 
    sa.guid = IDGen.get_uuid()
    sa.name = 'SBAC-{}-{}'.format(subject, grade)
    sa.id = '(SBAC){}-{}-{}-{}'.format(sa.name, 'Spring' if asmt_type == 'SUMMATIVE' else 'Winter', asmt_year - 1, asmt_year)
    sa.subject = subject
    sa.grade = grade
    sa.rec_id = id_gen.get_rec_id('assessment')
    sa.type = asmt_type
    sa.year = asmt_year
    sa.version = cfg.ASMT_VERSION
    sa.subject = subject
    sa.overall = Scorable('Overall', 'Overall', asmt_scale_scores[0], asmt_scale_scores[4], asmt_scale_scores[1:-1])
    sa.claims = [Scorable(claim['code'], claim['name'], asmt_scale_scores[0], asmt_scale_scores[-1]) for claim in claims]
    sa.effective_date = datetime.date(asmt_year - 1, 8, 15)
    sa.from_date = from_date if from_date is not None else sa.effective_date
    sa.to_date = to_date if to_date is not None else cfg.ASMT_TO_DATE
    generate_segment_and_item_bank(sa, gen_item, cfg.ASMT_ITEM_BANK_SIZE, id_gen)

    return sa


def generate_segment_and_item_bank(asmt: Assessment, gen_item, size, id_gen: IDGen):
    if not gen_item:
        asmt.segment = None
        asmt.item_bank = []
        asmt.item_total_score = None
        return

    # make a set of difficulty ranges favoring easy (x2), moderate (x3), hard (x1)
    diff_low = -3.0
    diff_mod = -2.5 + 0.2 * asmt.grade
    diff_hard = -1.25 + 0.25 * asmt.grade
    diff_high = 4.0
    diff_ranges = [(diff_low, diff_mod), (diff_low, diff_mod), (diff_mod, diff_hard), (diff_mod, diff_hard),
                   (diff_mod, diff_hard), (diff_hard, diff_high)]

    segment = AssessmentSegment()
    segment.id = id_gen.get_uuid()

    item_bank = []
    for i in range(size):
        item = AssessmentItem()
        item.position = i + 1
        item.bank_key = '200'
        item.item_key = str(id_gen.get_rec_id('asmt_item_id'))
        item.segment_id = segment.id
        item.type = choice(cfg.ASMT_ITEM_BANK_FORMAT)
        if item.type == 'MC':
            item.options_count = 4
            item.answer_key = choice(ascii_uppercase[0:4])
        if item.type == 'MS':
            item.options_count = 6
            item.answer_key = ','.join(sorted(sample(ascii_uppercase[0:6], 2)))
        item.max_score = 1
        item.dok = choice([1, 1, 1, 2, 2, 2, 3, 3, 4])
        dr = choice(diff_ranges)
        item.difficulty = dr[0] + random() * (dr[1] - dr[0])
        item.operational = '1'
        item_bank.append(item)

    asmt.segment = segment
    asmt.item_bank = item_bank
    asmt.item_total_score = sum(map(lambda x: x.max_score, item_bank))
