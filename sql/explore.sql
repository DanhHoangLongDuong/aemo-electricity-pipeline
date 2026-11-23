-- Check how many different RUNNO values exist
SELECT RUNNO,
       COUNT(RUNNO)
FROM `aemo-pipeline.raw.price`
GROUP BY RUNNO;

SELECT RUNNO,
       COUNT(RUNNO)
FROM `aemo-pipeline.raw.region_sum`
GROUP BY RUNNO;

-- Check how many different INTERVETION values exist
SELECT INTERVENTION,
       COUNT(INTERVENTION)
FROM `aemo-pipeline.raw.price`
GROUP BY INTERVENTION;

SELECT INTERVENTION,
       COUNT(INTERVENTION)
FROM `aemo-pipeline.raw.region_sum`
GROUP BY INTERVENTION;

-- Check how many SETTLEMENTDATE and REGIONID combinations exist that has more than one row
SELECT SETTLEMENTDATE,
       REGIONID,
       COUNT(*)
FROM `aemo-pipeline.raw.price`
GROUP BY SETTLEMENTDATE, REGIONID
HAVING COUNT(*) > 1;

SELECT SETTLEMENTDATE,
       REGIONID,
       COUNT(*)
FROM `aemo-pipeline.raw.region_sum`
GROUP BY SETTLEMENTDATE, REGIONID
HAVING COUNT(*) > 1;