-- query for pulling hierarchy out of an RDW warehouse
--
-- NOTE the check against natural-id length which is no longer appropriate

SELECT
  '06' AS state_id,
  'CA' AS state_code,
  'California' AS state_name,
  'california' AS state_type,
  d.natural_id AS district_id,
  d.name AS district_name,
  'Big Average' AS district_type,
  s.natural_id AS school_id,
  s.name AS school_name,
  CASE
    WHEN s.name LIKE '%High Sch' OR s.name LIKE '%High School' OR s.name LIKE '%High' OR s.name LIKE '%HS' OR s.name LIKE '%Senior High' THEN 'High School'
    WHEN s.name LIKE '%Middle School' OR s.name LIKE '%Middle' OR s.name LIKE '%Junior High' OR s.name LIKE '%Intermediate School' OR s.name LIKE '%MS' THEN 'Middle School'
    WHEN s.name LIKE '%Elem' OR s.name LIKE '%Sch' OR s.name LIKE '%Ctr' OR s.name LIKE '%Elementary School' OR s.name LIKE '%Primary' OR s.name LIKE '%Elementary' THEN 'Elementary School'
    ELSE NULL
  END AS school_type,
  'True' AS school_interims
FROM school s JOIN district d on s.district_id = d.id
WHERE LENGTH(s.natural_id) = 30 AND LENGTH(d.natural_id) = 30;