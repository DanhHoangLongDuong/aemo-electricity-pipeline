SET @@location = 'australia-southeast1';

SELECT MARKET_DAY,
       REGIONID,
       AVG(RRP) AS avg_rrp,
       MIN(RRP) AS min_rrp,
       MAX(RRP) AS max_rrp,
       COUNTIF(RRP > 300) rrp_intervals_above_300,
       COUNTIF(RRP > 5000) AS rrp_intervals_above_5000,
       COUNTIF(RRP < 0) AS rrp_intervals_below_0
FROM `aemo-pipeline.staging.stg_price`
GROUP BY MARKET_DAY, REGIONID
ORDER BY MARKET_DAY ASC;