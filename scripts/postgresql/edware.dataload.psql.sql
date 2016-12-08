COPY edware_ca.dim_asmt (asmt_rec_id, asmt_guid, asmt_type, asmt_period, asmt_period_year, asmt_version, asmt_subject, effective_date, asmt_claim_1_name, asmt_claim_2_name, asmt_claim_3_name, asmt_claim_4_name, asmt_perf_lvl_name_1,        asmt_perf_lvl_name_2, asmt_perf_lvl_name_3, asmt_perf_lvl_name_4, 
       asmt_perf_lvl_name_5, asmt_claim_perf_lvl_name_1, asmt_claim_perf_lvl_name_2, 
       asmt_claim_perf_lvl_name_3, asmt_score_min, asmt_score_max, asmt_claim_1_score_min, 
       asmt_claim_1_score_max, asmt_claim_2_score_min, asmt_claim_2_score_max, 
       asmt_claim_3_score_min, asmt_claim_3_score_max, asmt_claim_4_score_min, 
       asmt_claim_4_score_max, asmt_cut_point_1, asmt_cut_point_2, asmt_cut_point_3, 
       asmt_cut_point_4, from_date, to_date, rec_status, batch_guid) 
    from '/Users/allagorina/development/dw_datagenerator/out/dim_asmt.csv' DELIMITER ',' CSV HEADER;
       
COPY edware_ca.dim_inst_hier(inst_hier_rec_id, state_code, district_id, district_name, school_id,  
	  school_name, from_date, to_date, rec_status, batch_guid) 
	from '/Users/allagorina/development/dw_datagenerator/out/dim_inst_hier.csv' DELIMITER ',' CSV HEADER;       

COPY edware_ca.dim_student (student_rec_id, student_id, external_student_id, first_name, 
       middle_name, last_name, birthdate, sex, 
       dmg_eth_derived, dmg_eth_hsp, 
       dmg_eth_ami, dmg_eth_asn, dmg_eth_blk, dmg_eth_pcf, dmg_eth_wht, 
       dmg_eth_2om, dmg_prg_iep, dmg_prg_lep, dmg_prg_504, dmg_sts_ecd, 
       dmg_sts_mig, from_date, to_date, rec_status, batch_guid,
       group_1_id, group_1_text, 
       group_2_id, group_2_text, group_3_id, group_3_text, group_4_id, 
       group_4_text, group_5_id, group_5_text, group_6_id, group_6_text, 
       group_7_id, group_7_text, group_8_id, group_8_text, group_9_id, 
       group_9_text, group_10_id, group_10_text)
    from '/Users/allagorina/development/dw_datagenerator/out/dim_student.csv' DELIMITER ',' CSV HEADER;  
      
COPY edware_ca.fact_asmt_outcome ( asmt_outcome_rec_id,asmt_rec_id,student_rec_id,inst_hier_rec_id,asmt_guid,
       student_id,state_code,district_id,school_id,where_taken_id,where_taken_name,asmt_grade,enrl_grade,date_taken,
       date_taken_day,date_taken_month,date_taken_year,asmt_score,asmt_score_range_min,asmt_score_range_max,asmt_perf_lvl,
       asmt_claim_1_score,asmt_claim_1_score_range_min,asmt_claim_1_score_range_max,asmt_claim_1_perf_lvl,
       asmt_claim_2_score,asmt_claim_2_score_range_min,asmt_claim_2_score_range_max,asmt_claim_2_perf_lvl,
       asmt_claim_3_score,asmt_claim_3_score_range_min,asmt_claim_3_score_range_max,asmt_claim_3_perf_lvl,
       asmt_claim_4_score,asmt_claim_4_score_range_min,asmt_claim_4_score_range_max,asmt_claim_4_perf_lvl,
       acc_asl_video_embed,acc_print_on_demand_items_nonembed,acc_noise_buffer_nonembed,acc_braile_embed,
       acc_closed_captioning_embed,acc_text_to_speech_embed,acc_abacus_nonembed,acc_alternate_response_options_nonembed,
       acc_calculator_nonembed,acc_multiplication_table_nonembed,acc_print_on_demand_nonembed,acc_read_aloud_nonembed,
       acc_scribe_nonembed,acc_speech_to_text_nonembed,acc_streamline_mode,from_date,to_date,rec_status,batch_guid)
    from '/Users/allagorina/development/dw_datagenerator/out/fact_asmt_outcome.csv' DELIMITER ',' CSV HEADER; 
       
COPY edware_ca.fact_asmt_outcome_vw (asmt_outcome_vw_rec_id,asmt_rec_id,student_rec_id,inst_hier_rec_id,asmt_guid,
       student_id,state_code,district_id,school_id,where_taken_id,where_taken_name,asmt_type,asmt_year,asmt_subject,
       asmt_grade,enrl_grade,date_taken,date_taken_day,date_taken_month,date_taken_year,asmt_score,asmt_score_range_min,
       asmt_score_range_max,asmt_perf_lvl,asmt_claim_1_score,asmt_claim_1_score_range_min,asmt_claim_1_score_range_max,
       asmt_claim_1_perf_lvl,asmt_claim_2_score,asmt_claim_2_score_range_min,asmt_claim_2_score_range_max,
       asmt_claim_2_perf_lvl,asmt_claim_3_score,asmt_claim_3_score_range_min,asmt_claim_3_score_range_max,
       asmt_claim_3_perf_lvl,asmt_claim_4_score,asmt_claim_4_score_range_min,asmt_claim_4_score_range_max,
       asmt_claim_4_perf_lvl,sex,dmg_eth_derived,dmg_eth_hsp,dmg_eth_ami,dmg_eth_asn,dmg_eth_blk,
       dmg_eth_pcf,dmg_eth_wht,dmg_eth_2om,dmg_prg_iep,dmg_prg_lep,dmg_prg_504,dmg_sts_ecd,
       dmg_sts_mig,acc_asl_video_embed,acc_print_on_demand_items_nonembed,
       acc_noise_buffer_nonembed,acc_braile_embed,acc_closed_captioning_embed,
       acc_text_to_speech_embed,acc_abacus_nonembed,acc_alternate_response_options_nonembed,
       acc_calculator_nonembed,acc_multiplication_table_nonembed,acc_print_on_demand_nonembed,
       acc_read_aloud_nonembed,acc_scribe_nonembed,acc_speech_to_text_nonembed,acc_streamline_mode,
       from_date,to_date,rec_status,batch_guid)
    from '/Users/allagorina/development/dw_datagenerator/out/fact_asmt_outcome_vw.csv' DELIMITER ',' CSV HEADER; 
     
COPY edware_ca.fact_block_asmt_outcome (asmt_outcome_rec_id,asmt_rec_id,student_rec_id,inst_hier_rec_id,
       asmt_guid,student_id,state_code,district_id,school_id,where_taken_id,where_taken_name,asmt_type,asmt_year,
       asmt_subject,asmt_grade,enrl_grade,date_taken,date_taken_day,date_taken_month,date_taken_year,
       asmt_claim_1_score,asmt_claim_1_score_range_min,asmt_claim_1_score_range_max,asmt_claim_1_perf_lvl,sex,
       acc_asl_video_embed,acc_print_on_demand_items_nonembed,acc_noise_buffer_nonembed,acc_braile_embed,
       acc_closed_captioning_embed,acc_text_to_speech_embed,acc_abacus_nonembed,acc_alternate_response_options_nonembed,
       acc_calculator_nonembed,acc_multiplication_table_nonembed,acc_print_on_demand_nonembed,acc_read_aloud_nonembed,
       acc_scribe_nonembed,acc_speech_to_text_nonembed,acc_streamline_mode,from_date,to_date,rec_status,batch_guid)
    from '/Users/allagorina/development/dw_datagenerator/out/fact_block_asmt_outcome.csv' DELIMITER ',' CSV HEADER;       

COPY edware_ca.student_reg (student_reg_rec_id, state_code, state_name, district_id, district_name, 
       school_id, school_name, student_id, external_student_ssid, first_name, 
       middle_name, last_name, birthdate, sex, enrl_grade, dmg_eth_hsp, 
       dmg_eth_ami, dmg_eth_asn, dmg_eth_blk, dmg_eth_pcf, dmg_eth_wht, 
       dmg_multi_race, dmg_prg_iep, dmg_prg_lep, dmg_prg_504, dmg_sts_ecd, 
       dmg_sts_mig, confirm_code, language_code, eng_prof_lvl, us_school_entry_date, 
       lep_entry_date, lep_exit_date, t3_program_type, prim_disability_type, 
       student_reg_guid, academic_year, extract_date, reg_system_id, 
       batch_guid) 
    from '/Users/allagorina/development/dw_datagenerator/out/student_reg.csv' DELIMITER ',' CSV HEADER;            