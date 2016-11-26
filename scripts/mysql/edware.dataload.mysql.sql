LOAD DATA LOCAL INFILE '/Users/allagorina/development/dw_datagenerator/out/dim_inst_hier.csv' INTO TABLE dim_inst_hier FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/allagorina/development/dw_datagenerator/out/dim_student.csv' INTO TABLE dim_student  FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/allagorina/development/dw_datagenerator/out/dim_asmt.csv' INTO TABLE dim_asmt  FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/allagorina/development/dw_datagenerator/out/student_reg.csv' INTO TABLE student_reg  FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/allagorina/development/dw_datagenerator/out/fact_asmt_outcome_vw.csv' INTO TABLE fact_asmt_outcome_vw  FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/allagorina/development/dw_datagenerator/out/fact_asmt_outcome.csv' INTO TABLE fact_asmt_outcome  FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/Users/allagorina/development/dw_datagenerator/out/fact_block_asmt_outcome.csv' INTO TABLE fact_block_asmt_outcome  FIELDS TERMINATED BY ',' IGNORE 1 LINES;
