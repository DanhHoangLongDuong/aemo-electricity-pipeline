SET @@location = 'australia-southeast1';

CREATE OR REPLACE VIEW `aemo-pipeline.staging.stg_region_sum` AS
SELECT SETTLEMENTDATE,
       REGIONID,
       TOTALDEMAND,
       CAST((DATETIME_SUB(SETTLEMENTDATE, INTERVAL 5 MINUTE)) AS DATE) AS MARKET_DAY
FROM `aemo-pipeline.raw.region_sum`
WHERE INTERVENTION = 0;