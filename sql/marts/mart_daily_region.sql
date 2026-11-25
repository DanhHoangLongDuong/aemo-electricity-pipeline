SET @@location = 'australia-southeast1';


CREATE OR REPLACE TABLE `aemo-pipeline.marts.mart_daily_region` AS (
  WITH mart_price AS (
    SELECT MARKET_DAY,
          REGIONID,
          AVG(RRP) AS avg_rrp,
          MIN(RRP) AS min_rrp,
          MAX(RRP) AS max_rrp,
          COUNTIF(RRP > 300) AS rrp_intervals_above_300,
          COUNTIF(RRP > 5000) AS rrp_intervals_above_5000,
          COUNTIF(RRP < 0) AS rrp_intervals_below_0
    FROM `aemo-pipeline.staging.stg_price`
    GROUP BY MARKET_DAY, REGIONID
  ),

  mart_region_sum AS (
    SELECT MARKET_DAY,
          REGIONID,
          MAX(TOTALDEMAND) AS max_total_demand
    FROM `aemo-pipeline.staging.stg_region_sum`
    GROUP BY MARKET_DAY, REGIONID
  )

  SELECT COALESCE(marts_price.MARKET_DAY, marts_region_sum.MARKET_DAY) AS MARKET_DAY,
         COALESCE(marts_price.REGIONID, marts_region_sum.REGIONID) AS REGIONID,
         marts_price.avg_rrp,
         marts_price.min_rrp,
         marts_price.max_rrp,
         marts_price.rrp_intervals_above_300,
         marts_price.rrp_intervals_above_5000,
         marts_price.rrp_intervals_below_0,
         marts_region_sum.max_total_demand
  FROM marts_price
  FULL OUTER JOIN marts_region_sum
  ON marts_price.MARKET_DAY = marts_region_sum.MARKET_DAY
  AND marts_price.REGIONID = marts_region_sum.REGIONID
  ORDER BY MARKET_DAY ASC
);