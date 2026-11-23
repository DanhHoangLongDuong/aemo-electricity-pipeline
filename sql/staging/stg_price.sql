SET @@location = 'australia-southeast1';

CREATE OR REPLACE VIEW `aemo-pipeline.staging.stg_price` AS
SELECT SETTLEMENTDATE,
       REGIONID,
       RRP,
       CAST((DATETIME_SUB(SETTLEMENTDATE, INTERVAL 5 MINUTE)) AS DATE) AS MARKET_DAY
FROM `aemo-pipeline.raw.price`
WHERE INTERVENTION = 0;