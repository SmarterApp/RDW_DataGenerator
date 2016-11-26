--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: edware_ca; Type: SCHEMA; Schema: -; Owner: edware
--

CREATE SCHEMA edware_ca;


ALTER SCHEMA edware_ca OWNER TO edware;

SET search_path = edware_ca, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: custom_metadata; Type: TABLE; Schema: edware_ca; Owner: edware
--

CREATE TABLE custom_metadata (
    state_code character varying(2) NOT NULL,
    asmt_custom_metadata text
);


ALTER TABLE custom_metadata OWNER TO edware;

--
-- Name: dim_asmt; Type: TABLE; Schema: edware_ca; Owner: edware
--

CREATE TABLE dim_asmt (
    asmt_rec_id bigint NOT NULL,
    asmt_guid character varying(255) NOT NULL,
    asmt_type character varying(32) NOT NULL,
    asmt_period character varying(32),
    asmt_period_year smallint NOT NULL,
    asmt_version character varying(40) NOT NULL,
    asmt_subject character varying(64) NOT NULL,
    effective_date character varying(8) NOT NULL,
    asmt_claim_1_name character varying(128),
    asmt_claim_2_name character varying(128),
    asmt_claim_3_name character varying(128),
    asmt_claim_4_name character varying(128),
    asmt_perf_lvl_name_1 character varying(25),
    asmt_perf_lvl_name_2 character varying(25),
    asmt_perf_lvl_name_3 character varying(25),
    asmt_perf_lvl_name_4 character varying(25),
    asmt_perf_lvl_name_5 character varying(25),
    asmt_claim_perf_lvl_name_1 character varying(128),
    asmt_claim_perf_lvl_name_2 character varying(128),
    asmt_claim_perf_lvl_name_3 character varying(128),
    asmt_score_min smallint NOT NULL,
    asmt_score_max smallint NOT NULL,
    asmt_claim_1_score_min smallint NOT NULL,
    asmt_claim_1_score_max smallint NOT NULL,
    asmt_claim_2_score_min smallint NOT NULL,
    asmt_claim_2_score_max smallint NOT NULL,
    asmt_claim_3_score_min smallint NOT NULL,
    asmt_claim_3_score_max smallint NOT NULL,
    asmt_claim_4_score_min smallint,
    asmt_claim_4_score_max smallint,
    asmt_cut_point_1 smallint,
    asmt_cut_point_2 smallint,
    asmt_cut_point_3 smallint,
    asmt_cut_point_4 smallint,
    from_date character varying(8) NOT NULL,
    to_date character varying(8),
    rec_status character varying(1) NOT NULL,
    batch_guid character varying(36) NOT NULL
);


ALTER TABLE dim_asmt OWNER TO edware;

--
-- Name: dim_asmt_asmt_rec_id_seq; Type: SEQUENCE; Schema: edware_ca; Owner: edware
--

CREATE SEQUENCE dim_asmt_asmt_rec_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE dim_asmt_asmt_rec_id_seq OWNER TO edware;

--
-- Name: dim_asmt_asmt_rec_id_seq; Type: SEQUENCE OWNED BY; Schema: edware_ca; Owner: edware
--

ALTER SEQUENCE dim_asmt_asmt_rec_id_seq OWNED BY dim_asmt.asmt_rec_id;


--
-- Name: dim_inst_hier; Type: TABLE; Schema: edware_ca; Owner: edware
--

CREATE TABLE dim_inst_hier (
    inst_hier_rec_id bigint NOT NULL,
    state_code character varying(2) NOT NULL,
    district_id character varying(40) NOT NULL,
    district_name character varying(60) NOT NULL,
    school_id character varying(40) NOT NULL,
    school_name character varying(60) NOT NULL,
    from_date character varying(8) NOT NULL,
    to_date character varying(8),
    rec_status character varying(1) NOT NULL,
    batch_guid character varying(36) NOT NULL
);


ALTER TABLE dim_inst_hier OWNER TO edware;

--
-- Name: dim_inst_hier_inst_hier_rec_id_seq; Type: SEQUENCE; Schema: edware_ca; Owner: edware
--

CREATE SEQUENCE dim_inst_hier_inst_hier_rec_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE dim_inst_hier_inst_hier_rec_id_seq OWNER TO edware;

--
-- Name: dim_inst_hier_inst_hier_rec_id_seq; Type: SEQUENCE OWNED BY; Schema: edware_ca; Owner: edware
--

ALTER SEQUENCE dim_inst_hier_inst_hier_rec_id_seq OWNED BY dim_inst_hier.inst_hier_rec_id;


--
-- Name: dim_student; Type: TABLE; Schema: edware_ca; Owner: edware
--

CREATE TABLE dim_student (
    student_rec_id bigint NOT NULL,
    student_id character varying(40) NOT NULL,
    external_student_id character varying(40),
    first_name character varying(35),
    middle_name character varying(35),
    last_name character varying(35),
    birthdate character varying(8),
    sex character varying(10) NOT NULL,
    group_1_id character varying(40),
    group_1_text character varying(60),
    group_2_id character varying(40),
    group_2_text character varying(60),
    group_3_id character varying(40),
    group_3_text character varying(60),
    group_4_id character varying(40),
    group_4_text character varying(60),
    group_5_id character varying(40),
    group_5_text character varying(60),
    group_6_id character varying(40),
    group_6_text character varying(60),
    group_7_id character varying(40),
    group_7_text character varying(60),
    group_8_id character varying(40),
    group_8_text character varying(60),
    group_9_id character varying(40),
    group_9_text character varying(60),
    group_10_id character varying(40),
    group_10_text character varying(60),
    dmg_eth_derived smallint,
    dmg_eth_hsp boolean,
    dmg_eth_ami boolean,
    dmg_eth_asn boolean,
    dmg_eth_blk boolean,
    dmg_eth_pcf boolean,
    dmg_eth_wht boolean,
    dmg_eth_2om boolean,
    dmg_prg_iep boolean,
    dmg_prg_lep boolean,
    dmg_prg_504 boolean,
    dmg_sts_ecd boolean,
    dmg_sts_mig boolean,
    from_date character varying(8) NOT NULL,
    to_date character varying(8),
    rec_status character varying(1) NOT NULL,
    batch_guid character varying(36) NOT NULL
);


ALTER TABLE dim_student OWNER TO edware;

--
-- Name: dim_student_student_rec_id_seq; Type: SEQUENCE; Schema: edware_ca; Owner: edware
--

CREATE SEQUENCE dim_student_student_rec_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE dim_student_student_rec_id_seq OWNER TO edware;

--
-- Name: dim_student_student_rec_id_seq; Type: SEQUENCE OWNED BY; Schema: edware_ca; Owner: edware
--

ALTER SEQUENCE dim_student_student_rec_id_seq OWNED BY dim_student.student_rec_id;


--
-- Name: fact_asmt_outcome; Type: TABLE; Schema: edware_ca; Owner: edware
--

CREATE TABLE fact_asmt_outcome (
    asmt_outcome_rec_id bigint NOT NULL,
    asmt_rec_id bigint NOT NULL,
    student_rec_id bigint NOT NULL,
    inst_hier_rec_id bigint NOT NULL,
    asmt_guid character varying(255) NOT NULL,
    student_id character varying(40) NOT NULL,
    state_code character varying(2) NOT NULL,
    district_id character varying(40) NOT NULL,
    school_id character varying(40) NOT NULL,
    where_taken_id character varying(40),
    where_taken_name character varying(60),
    asmt_grade character varying(10) NOT NULL,
    enrl_grade character varying(10) NOT NULL,
    date_taken character varying(8) NOT NULL,
    date_taken_day smallint NOT NULL,
    date_taken_month smallint NOT NULL,
    date_taken_year smallint NOT NULL,
    asmt_score smallint NOT NULL,
    asmt_score_range_min smallint NOT NULL,
    asmt_score_range_max smallint NOT NULL,
    asmt_perf_lvl smallint NOT NULL,
    asmt_claim_1_score smallint,
    asmt_claim_1_score_range_min smallint,
    asmt_claim_1_score_range_max smallint,
    asmt_claim_1_perf_lvl smallint,
    asmt_claim_2_score smallint,
    asmt_claim_2_score_range_min smallint,
    asmt_claim_2_score_range_max smallint,
    asmt_claim_2_perf_lvl smallint,
    asmt_claim_3_score smallint,
    asmt_claim_3_score_range_min smallint,
    asmt_claim_3_score_range_max smallint,
    asmt_claim_3_perf_lvl smallint,
    asmt_claim_4_score smallint,
    asmt_claim_4_score_range_min smallint,
    asmt_claim_4_score_range_max smallint,
    asmt_claim_4_perf_lvl smallint,
    acc_asl_video_embed smallint NOT NULL,
    acc_braile_embed smallint NOT NULL,
    acc_closed_captioning_embed smallint NOT NULL,
    acc_text_to_speech_embed smallint NOT NULL,
    acc_abacus_nonembed smallint NOT NULL,
    acc_alternate_response_options_nonembed smallint NOT NULL,
    acc_calculator_nonembed smallint NOT NULL,
    acc_multiplication_table_nonembed smallint NOT NULL,
    acc_print_on_demand_nonembed smallint NOT NULL,
    acc_print_on_demand_items_nonembed smallint NOT NULL,
    acc_read_aloud_nonembed smallint NOT NULL,
    acc_scribe_nonembed smallint NOT NULL,
    acc_speech_to_text_nonembed smallint NOT NULL,
    acc_streamline_mode smallint NOT NULL,
    acc_noise_buffer_nonembed smallint NOT NULL,
    complete boolean,
    from_date character varying(8) NOT NULL,
    to_date character varying(8),
    rec_status character varying(2) NOT NULL,
    batch_guid character varying(36) NOT NULL,
    administration_condition character varying(2)
);


ALTER TABLE fact_asmt_outcome OWNER TO edware;

--
-- Name: fact_asmt_outcome_asmt_outcome_rec_id_seq; Type: SEQUENCE; Schema: edware_ca; Owner: edware
--

CREATE SEQUENCE fact_asmt_outcome_asmt_outcome_rec_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE fact_asmt_outcome_asmt_outcome_rec_id_seq OWNER TO edware;

--
-- Name: fact_asmt_outcome_asmt_outcome_rec_id_seq; Type: SEQUENCE OWNED BY; Schema: edware_ca; Owner: edware
--

ALTER SEQUENCE fact_asmt_outcome_asmt_outcome_rec_id_seq OWNED BY fact_asmt_outcome.asmt_outcome_rec_id;


--
-- Name: fact_asmt_outcome_vw; Type: TABLE; Schema: edware_ca; Owner: edware
--

CREATE TABLE fact_asmt_outcome_vw (
    asmt_outcome_vw_rec_id bigint NOT NULL,
    asmt_rec_id bigint NOT NULL,
    student_rec_id bigint NOT NULL,
    inst_hier_rec_id bigint NOT NULL,
    asmt_guid character varying(255) NOT NULL,
    student_id character varying(40) NOT NULL,
    state_code character varying(2) NOT NULL,
    district_id character varying(40) NOT NULL,
    school_id character varying(40) NOT NULL,
    where_taken_id character varying(40),
    where_taken_name character varying(60),
    asmt_type character varying(32) NOT NULL,
    asmt_year smallint NOT NULL,
    asmt_subject character varying(64) NOT NULL,
    asmt_grade character varying(10) NOT NULL,
    enrl_grade character varying(10) NOT NULL,
    date_taken character varying(8) NOT NULL,
    date_taken_day smallint NOT NULL,
    date_taken_month smallint NOT NULL,
    date_taken_year smallint NOT NULL,
    asmt_score smallint NOT NULL,
    asmt_score_range_min smallint NOT NULL,
    asmt_score_range_max smallint NOT NULL,
    asmt_perf_lvl smallint NOT NULL,
    asmt_claim_1_score smallint,
    asmt_claim_1_score_range_min smallint,
    asmt_claim_1_score_range_max smallint,
    asmt_claim_1_perf_lvl smallint,
    asmt_claim_2_score smallint,
    asmt_claim_2_score_range_min smallint,
    asmt_claim_2_score_range_max smallint,
    asmt_claim_2_perf_lvl smallint,
    asmt_claim_3_score smallint,
    asmt_claim_3_score_range_min smallint,
    asmt_claim_3_score_range_max smallint,
    asmt_claim_3_perf_lvl smallint,
    asmt_claim_4_score smallint,
    asmt_claim_4_score_range_min smallint,
    asmt_claim_4_score_range_max smallint,
    asmt_claim_4_perf_lvl smallint,
    sex character varying(10) NOT NULL,
    dmg_eth_derived smallint,
    dmg_eth_hsp boolean,
    dmg_eth_ami boolean,
    dmg_eth_asn boolean,
    dmg_eth_blk boolean,
    dmg_eth_pcf boolean,
    dmg_eth_wht boolean,
    dmg_eth_2om boolean,
    dmg_prg_iep boolean,
    dmg_prg_lep boolean,
    dmg_prg_504 boolean,
    dmg_sts_ecd boolean,
    dmg_sts_mig boolean,
    acc_asl_video_embed smallint NOT NULL,
    acc_braile_embed smallint NOT NULL,
    acc_closed_captioning_embed smallint NOT NULL,
    acc_text_to_speech_embed smallint NOT NULL,
    acc_abacus_nonembed smallint NOT NULL,
    acc_alternate_response_options_nonembed smallint NOT NULL,
    acc_calculator_nonembed smallint NOT NULL,
    acc_multiplication_table_nonembed smallint NOT NULL,
    acc_print_on_demand_nonembed smallint NOT NULL,
    acc_print_on_demand_items_nonembed smallint NOT NULL,
    acc_read_aloud_nonembed smallint NOT NULL,
    acc_scribe_nonembed smallint NOT NULL,
    acc_speech_to_text_nonembed smallint NOT NULL,
    acc_streamline_mode smallint NOT NULL,
    acc_noise_buffer_nonembed smallint NOT NULL,
    complete boolean,
    from_date character varying(8) NOT NULL,
    to_date character varying(8),
    rec_status character varying(1) NOT NULL,
    batch_guid character varying(36) NOT NULL,
    administration_condition character varying(2)
);


ALTER TABLE fact_asmt_outcome_vw OWNER TO edware;

--
-- Name: fact_asmt_outcome_vw_asmt_outcome_vw_rec_id_seq; Type: SEQUENCE; Schema: edware_ca; Owner: edware
--

CREATE SEQUENCE fact_asmt_outcome_vw_asmt_outcome_vw_rec_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE fact_asmt_outcome_vw_asmt_outcome_vw_rec_id_seq OWNER TO edware;

--
-- Name: fact_asmt_outcome_vw_asmt_outcome_vw_rec_id_seq; Type: SEQUENCE OWNED BY; Schema: edware_ca; Owner: edware
--

ALTER SEQUENCE fact_asmt_outcome_vw_asmt_outcome_vw_rec_id_seq OWNED BY fact_asmt_outcome_vw.asmt_outcome_vw_rec_id;


--
-- Name: fact_block_asmt_outcome; Type: TABLE; Schema: edware_ca; Owner: edware
--

CREATE TABLE fact_block_asmt_outcome (
    asmt_outcome_rec_id bigint NOT NULL,
    asmt_rec_id bigint NOT NULL,
    student_rec_id bigint NOT NULL,
    inst_hier_rec_id bigint NOT NULL,
    asmt_guid character varying(255) NOT NULL,
    student_id character varying(40) NOT NULL,
    state_code character varying(2) NOT NULL,
    district_id character varying(40) NOT NULL,
    school_id character varying(40) NOT NULL,
    where_taken_id character varying(40),
    where_taken_name character varying(60),
    asmt_type character varying(32) NOT NULL,
    asmt_year smallint NOT NULL,
    asmt_subject character varying(64) NOT NULL,
    asmt_grade character varying(10) NOT NULL,
    enrl_grade character varying(10) NOT NULL,
    date_taken character varying(8) NOT NULL,
    date_taken_day smallint NOT NULL,
    date_taken_month smallint NOT NULL,
    date_taken_year smallint NOT NULL,
    asmt_claim_1_score smallint,
    asmt_claim_1_score_range_min smallint,
    asmt_claim_1_score_range_max smallint,
    asmt_claim_1_perf_lvl smallint,
    sex character varying(10) NOT NULL,
    dmg_eth_derived smallint,
    dmg_eth_hsp boolean,
    dmg_eth_ami boolean,
    dmg_eth_asn boolean,
    dmg_eth_blk boolean,
    dmg_eth_pcf boolean,
    dmg_eth_wht boolean,
    dmg_eth_2om boolean,
    dmg_prg_iep boolean,
    dmg_prg_lep boolean,
    dmg_prg_504 boolean,
    dmg_sts_ecd boolean,
    dmg_sts_mig boolean,
    acc_asl_video_embed smallint NOT NULL,
    acc_braile_embed smallint NOT NULL,
    acc_closed_captioning_embed smallint NOT NULL,
    acc_text_to_speech_embed smallint NOT NULL,
    acc_abacus_nonembed smallint NOT NULL,
    acc_alternate_response_options_nonembed smallint NOT NULL,
    acc_calculator_nonembed smallint NOT NULL,
    acc_multiplication_table_nonembed smallint NOT NULL,
    acc_print_on_demand_nonembed smallint NOT NULL,
    acc_print_on_demand_items_nonembed smallint NOT NULL,
    acc_read_aloud_nonembed smallint NOT NULL,
    acc_scribe_nonembed smallint NOT NULL,
    acc_speech_to_text_nonembed smallint NOT NULL,
    acc_streamline_mode smallint NOT NULL,
    acc_noise_buffer_nonembed smallint NOT NULL,
    complete boolean,
    from_date character varying(8) NOT NULL,
    to_date character varying(8),
    rec_status character varying(1) NOT NULL,
    batch_guid character varying(36) NOT NULL,
    administration_condition character varying(2)
);


ALTER TABLE fact_block_asmt_outcome OWNER TO edware;

--
-- Name: fact_block_asmt_outcome_asmt_outcome_rec_id_seq; Type: SEQUENCE; Schema: edware_ca; Owner: edware
--

CREATE SEQUENCE fact_block_asmt_outcome_asmt_outcome_rec_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE fact_block_asmt_outcome_asmt_outcome_rec_id_seq OWNER TO edware;

--
-- Name: fact_block_asmt_outcome_asmt_outcome_rec_id_seq; Type: SEQUENCE OWNED BY; Schema: edware_ca; Owner: edware
--

ALTER SEQUENCE fact_block_asmt_outcome_asmt_outcome_rec_id_seq OWNED BY fact_block_asmt_outcome.asmt_outcome_rec_id;


--
-- Name: global_rec_seq; Type: SEQUENCE; Schema: edware_ca; Owner: edware
--

CREATE SEQUENCE global_rec_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE global_rec_seq OWNER TO edware;

--
-- Name: student_reg; Type: TABLE; Schema: edware_ca; Owner: edware
--

CREATE TABLE student_reg (
    student_reg_rec_id bigint NOT NULL,
    state_code character varying(2) NOT NULL,
    state_name character varying(50) NOT NULL,
    district_id character varying(40) NOT NULL,
    district_name character varying(60) NOT NULL,
    school_id character varying(40) NOT NULL,
    school_name character varying(60) NOT NULL,
    student_id character varying(40) NOT NULL,
    external_student_ssid character varying(40) NOT NULL,
    first_name character varying(35),
    middle_name character varying(35),
    last_name character varying(35),
    birthdate character varying(10),
    sex character varying(10) NOT NULL,
    enrl_grade character varying(10) NOT NULL,
    dmg_eth_hsp boolean,
    dmg_eth_ami boolean,
    dmg_eth_asn boolean,
    dmg_eth_blk boolean,
    dmg_eth_pcf boolean,
    dmg_eth_wht boolean,
    dmg_multi_race boolean,
    dmg_prg_iep boolean,
    dmg_prg_lep boolean,
    dmg_prg_504 boolean,
    dmg_sts_ecd boolean,
    dmg_sts_mig boolean,
    confirm_code character varying(50),
    language_code character varying(3),
    eng_prof_lvl character varying(20),
    us_school_entry_date character varying(10),
    lep_entry_date character varying(10),
    lep_exit_date character varying(10),
    t3_program_type character varying(27),
    prim_disability_type character varying(3),
    student_reg_guid character varying(50) NOT NULL,
    academic_year smallint NOT NULL,
    extract_date character varying(10) NOT NULL,
    reg_system_id character varying(40) NOT NULL,
    batch_guid character varying(36) NOT NULL
);


ALTER TABLE student_reg OWNER TO edware;

--
-- Name: student_reg_student_reg_rec_id_seq; Type: SEQUENCE; Schema: edware_ca; Owner: edware
--

CREATE SEQUENCE student_reg_student_reg_rec_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE student_reg_student_reg_rec_id_seq OWNER TO edware;

--
-- Name: student_reg_student_reg_rec_id_seq; Type: SEQUENCE OWNED BY; Schema: edware_ca; Owner: edware
--

ALTER SEQUENCE student_reg_student_reg_rec_id_seq OWNED BY student_reg.student_reg_rec_id;


--
-- Name: asmt_rec_id; Type: DEFAULT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY dim_asmt ALTER COLUMN asmt_rec_id SET DEFAULT nextval('dim_asmt_asmt_rec_id_seq'::regclass);


--
-- Name: inst_hier_rec_id; Type: DEFAULT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY dim_inst_hier ALTER COLUMN inst_hier_rec_id SET DEFAULT nextval('dim_inst_hier_inst_hier_rec_id_seq'::regclass);


--
-- Name: student_rec_id; Type: DEFAULT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY dim_student ALTER COLUMN student_rec_id SET DEFAULT nextval('dim_student_student_rec_id_seq'::regclass);


--
-- Name: asmt_outcome_rec_id; Type: DEFAULT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome ALTER COLUMN asmt_outcome_rec_id SET DEFAULT nextval('fact_asmt_outcome_asmt_outcome_rec_id_seq'::regclass);


--
-- Name: asmt_outcome_vw_rec_id; Type: DEFAULT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome_vw ALTER COLUMN asmt_outcome_vw_rec_id SET DEFAULT nextval('fact_asmt_outcome_vw_asmt_outcome_vw_rec_id_seq'::regclass);


--
-- Name: asmt_outcome_rec_id; Type: DEFAULT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_block_asmt_outcome ALTER COLUMN asmt_outcome_rec_id SET DEFAULT nextval('fact_block_asmt_outcome_asmt_outcome_rec_id_seq'::regclass);


--
-- Name: student_reg_rec_id; Type: DEFAULT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY student_reg ALTER COLUMN student_reg_rec_id SET DEFAULT nextval('student_reg_student_reg_rec_id_seq'::regclass);


--
-- Name: dim_asmt_pkey; Type: CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY dim_asmt
    ADD CONSTRAINT dim_asmt_pkey PRIMARY KEY (asmt_rec_id);


--
-- Name: dim_inst_hier_pkey; Type: CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY dim_inst_hier
    ADD CONSTRAINT dim_inst_hier_pkey PRIMARY KEY (inst_hier_rec_id);


--
-- Name: dim_student_pkey; Type: CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY dim_student
    ADD CONSTRAINT dim_student_pkey PRIMARY KEY (student_rec_id);


--
-- Name: fact_asmt_outcome_pkey; Type: CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome
    ADD CONSTRAINT fact_asmt_outcome_pkey PRIMARY KEY (asmt_outcome_rec_id);


--
-- Name: fact_asmt_outcome_vw_pkey; Type: CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome_vw
    ADD CONSTRAINT fact_asmt_outcome_vw_pkey PRIMARY KEY (asmt_outcome_vw_rec_id);


--
-- Name: fact_block_asmt_outcome_pkey; Type: CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_block_asmt_outcome
    ADD CONSTRAINT fact_block_asmt_outcome_pkey PRIMARY KEY (asmt_outcome_rec_id);


--
-- Name: student_reg_pkey; Type: CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY student_reg
    ADD CONSTRAINT student_reg_pkey PRIMARY KEY (student_reg_rec_id);


--
-- Name: custom_metadata_id_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE UNIQUE INDEX custom_metadata_id_idx ON custom_metadata USING btree (state_code);


--
-- Name: dim_asmt_guid_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX dim_asmt_guid_idx ON dim_asmt USING btree (asmt_guid);


--
-- Name: dim_asmt_id_type_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX dim_asmt_id_type_idx ON dim_asmt USING btree (asmt_rec_id, asmt_type);


--
-- Name: dim_asmt_rec_pk_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE UNIQUE INDEX dim_asmt_rec_pk_idx ON dim_asmt USING btree (asmt_rec_id);


--
-- Name: dim_inst_hier_codex; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX dim_inst_hier_codex ON dim_inst_hier USING btree (state_code, district_id, school_id);


--
-- Name: dim_inst_hier_rec_pk_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE UNIQUE INDEX dim_inst_hier_rec_pk_idx ON dim_inst_hier USING btree (inst_hier_rec_id);


--
-- Name: dim_student_id_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX dim_student_id_idx ON dim_student USING btree (student_id);


--
-- Name: dim_student_rec_pk_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE UNIQUE INDEX dim_student_rec_pk_idx ON dim_student USING btree (student_rec_id);


--
-- Name: fact_asmt_outcome_student_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_student_idx ON fact_asmt_outcome USING btree (student_id, asmt_guid, date_taken);


--
-- Name: fact_asmt_outcome_vw_504_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_504_idx ON fact_asmt_outcome_vw USING btree (dmg_prg_504);


--
-- Name: fact_asmt_outcome_vw_asmt_subj_typ_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_asmt_subj_typ_idx ON fact_asmt_outcome_vw USING btree (student_id, asmt_subject, asmt_type);


--
-- Name: fact_asmt_outcome_vw_cpop_not_stated_count_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_cpop_not_stated_count_idx ON fact_asmt_outcome_vw USING btree (rec_status, asmt_type, asmt_year, state_code, district_id, school_id, dmg_prg_iep, dmg_prg_504, dmg_prg_lep, dmg_sts_mig, asmt_grade, dmg_eth_derived, sex, administration_condition);


--
-- Name: fact_asmt_outcome_vw_cpop_stateview_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_cpop_stateview_idx ON fact_asmt_outcome_vw USING btree (state_code, asmt_type, rec_status, asmt_year, inst_hier_rec_id, asmt_subject, asmt_perf_lvl, district_id, asmt_grade, administration_condition);


--
-- Name: fact_asmt_outcome_vw_ecd_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_ecd_idx ON fact_asmt_outcome_vw USING btree (dmg_sts_ecd);


--
-- Name: fact_asmt_outcome_vw_eth_derived_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_eth_derived_idx ON fact_asmt_outcome_vw USING btree (dmg_eth_derived);


--
-- Name: fact_asmt_outcome_vw_grade_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_grade_idx ON fact_asmt_outcome_vw USING btree (asmt_grade);


--
-- Name: fact_asmt_outcome_vw_iep_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_iep_idx ON fact_asmt_outcome_vw USING btree (dmg_prg_iep);


--
-- Name: fact_asmt_outcome_vw_lep_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_lep_idx ON fact_asmt_outcome_vw USING btree (dmg_prg_lep);


--
-- Name: fact_asmt_outcome_vw_mig_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_mig_idx ON fact_asmt_outcome_vw USING btree (dmg_sts_mig);


--
-- Name: fact_asmt_outcome_vw_sex_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_sex_idx ON fact_asmt_outcome_vw USING btree (sex);


--
-- Name: fact_asmt_outcome_vw_student_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_asmt_outcome_vw_student_idx ON fact_asmt_outcome_vw USING btree (student_id, asmt_guid, date_taken, administration_condition);


--
-- Name: fact_block_asmt_outcome_report_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_block_asmt_outcome_report_idx ON fact_block_asmt_outcome USING btree (state_code, school_id, district_id, asmt_year, rec_status, asmt_type, asmt_grade, asmt_subject);


--
-- Name: fact_block_asmt_outcome_student_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX fact_block_asmt_outcome_student_idx ON fact_block_asmt_outcome USING btree (student_id, asmt_guid, date_taken);


--
-- Name: student_reg_guid_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX student_reg_guid_idx ON student_reg USING btree (student_id);


--
-- Name: student_reg_year_system_idx; Type: INDEX; Schema: edware_ca; Owner: edware
--

CREATE INDEX student_reg_year_system_idx ON student_reg USING btree (academic_year, reg_system_id);


--
-- Name: fact_asmt_outcome_asmt_rec_id_fkey; Type: FK CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome
    ADD CONSTRAINT fact_asmt_outcome_asmt_rec_id_fkey FOREIGN KEY (asmt_rec_id) REFERENCES dim_asmt(asmt_rec_id);


--
-- Name: fact_asmt_outcome_inst_hier_rec_id_fkey; Type: FK CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome
    ADD CONSTRAINT fact_asmt_outcome_inst_hier_rec_id_fkey FOREIGN KEY (inst_hier_rec_id) REFERENCES dim_inst_hier(inst_hier_rec_id);


--
-- Name: fact_asmt_outcome_student_rec_id_fkey; Type: FK CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome
    ADD CONSTRAINT fact_asmt_outcome_student_rec_id_fkey FOREIGN KEY (student_rec_id) REFERENCES dim_student(student_rec_id);


--
-- Name: fact_asmt_outcome_vw_asmt_rec_id_fkey; Type: FK CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome_vw
    ADD CONSTRAINT fact_asmt_outcome_vw_asmt_rec_id_fkey FOREIGN KEY (asmt_rec_id) REFERENCES dim_asmt(asmt_rec_id);


--
-- Name: fact_asmt_outcome_vw_inst_hier_rec_id_fkey; Type: FK CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome_vw
    ADD CONSTRAINT fact_asmt_outcome_vw_inst_hier_rec_id_fkey FOREIGN KEY (inst_hier_rec_id) REFERENCES dim_inst_hier(inst_hier_rec_id);


--
-- Name: fact_asmt_outcome_vw_student_rec_id_fkey; Type: FK CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_asmt_outcome_vw
    ADD CONSTRAINT fact_asmt_outcome_vw_student_rec_id_fkey FOREIGN KEY (student_rec_id) REFERENCES dim_student(student_rec_id);


--
-- Name: fact_block_asmt_outcome_asmt_rec_id_fkey; Type: FK CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_block_asmt_outcome
    ADD CONSTRAINT fact_block_asmt_outcome_asmt_rec_id_fkey FOREIGN KEY (asmt_rec_id) REFERENCES dim_asmt(asmt_rec_id);


--
-- Name: fact_block_asmt_outcome_inst_hier_rec_id_fkey; Type: FK CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_block_asmt_outcome
    ADD CONSTRAINT fact_block_asmt_outcome_inst_hier_rec_id_fkey FOREIGN KEY (inst_hier_rec_id) REFERENCES dim_inst_hier(inst_hier_rec_id);


--
-- Name: fact_block_asmt_outcome_student_rec_id_fkey; Type: FK CONSTRAINT; Schema: edware_ca; Owner: edware
--

ALTER TABLE ONLY fact_block_asmt_outcome
    ADD CONSTRAINT fact_block_asmt_outcome_student_rec_id_fkey FOREIGN KEY (student_rec_id) REFERENCES dim_student(student_rec_id);


--
-- PostgreSQL database dump complete
--

