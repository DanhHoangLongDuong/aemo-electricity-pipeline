## 1. Setup
1. (2026-11-14) Use Python `3.14` on the runner.
Reason: ubuntu-latest can not use `3.14.3`, so change to `3.14`.
2. (2026-11-14) Use workflow_dispatch instead of push.\
Reason: If use push, the workflow runs everytime the project is pushed. \
Change to workflow_dispatch for manually testing the workflow.
3. (2026-11-14) The download_file_test result: NEMWEB is reachable from GitHub Actions. 
4. (2026-11-14) Keep the original zip, never overwrite.
## 2. Explore
5. (2026-11-15) price_df table:
    - `SETTLEMENTDATE`: Key, the end of the 5-minute interval.
    - `REGIONID`: Key, region.
    - `RUNNO`: Key, dispatch run number.
    - `INTERVENTION`: Key, 1 means AEMO orders to run, not market's choice. 0 means the market price.\
    Staging (4.1) keeps only `INTERVENTION = 0`, so it has one row per time and region.
    - `RRP`: Measure, regional Reference Price. Every price mart uses it.
    - `PRICE_STATUS`: Quality, to know if the RRP is firm or not.
    - `LASTCHANGED`: Quality, to know when is the last change of the price.
    - Row key: `SETTLEMENTDATE` + `REGIONID` + `RUNNO` + `INTERVENTION`.
    - Drop columns: 
        - `APCFLAG`, `MARKETSUSPENDEDFLAG`, `EEP`, `ROP`, `DISPATCHINTERVAL`: Out of scope/ duplicates.
        - FCAS columns: Out of scope.
6. (2026-11-15) regionsum_df table:
    - `SETTLEMENTDATE`: Key, the end of the 5-minute interval.
    - `REGIONID`: Key, region.
    - `RUNNO`: Key, dispatch run number.
    - `INTERVENTION`: Key, 1 means AEMO orders to run, not market's choice. 0 means the market price.\
    Staging (4.1) keeps only `INTERVENTION = 0`, so it has one row per time and region.
    -  `TOTALDEMAND`: Measure, total regional operational demand to be met.
    - Row key: `SETTLEMENTDATE` + `REGIONID` + `RUNNO` + `INTERVENTION`.
    - Drop columns:
        - `DEMANDFORECAST`, `AVAILABLEGENERATION`, `NETINTERCHANGE`: Out of scope.
        - FCAS columns: Out of scope.
7. (2026-11-15) Data types are decided in 2.2.
8. (2026-11-15) AEMO uses UTC+10 year-round. No Daylight Saving Time.
9. (2026-11-15) Store times in market time (UTC+10) as AEMO sends it: no DST so no ambiguity, daily marts group by the market day.
10. (2026-11-15) `00:00` row belong to the previous day.
## 3. BigQuery design
11. (2026-11-16) location is 'australia-southeast1'\
Reason: The data and the dashboard's audience are both in Australia, and all three datasets must share one location.
12. (2026-11-16) Use SQL to create datasets.\
Reason: Readable DDL
13. Use NUMERIC instead of FLOAT\
Reason: NUMERIC stores exact decimals, FLOAT can have rounding errors.
14. DATETIME for times\
Reason: market time, entry 9
## 4. Ingestion
15. One parse engine + column dict. The zip is read once per table
16. Retry only on timeout and connection errors
17. Only do 5 attempts, 3 second pause between them, if already do 5 attempts then re-raise
18. Skip if real file exists. Write to `.temp`, then rename\
Reason: A crash never leaves a half file under the real name
19. Idempotency: Delete by `source_file`, then append.\
The `00:00` row lands in the next day's partition, hence partition repace is not used.
20. `source_file`: file name only (not the path), so it is the same wherever the code runs
21. Types converted in `load.py`, and `Decimal` for `NUMERIC`, never via `float`
22. newest day = market today - 2. Measured: the archive file appears about 01:00 market time, two days later
23. "today" is computed in fixed UTC+10, so it's the same on any machine
24. A day counts as loaded only if it's in both tables
25. oldest first. One failed day doesn't stop the run. Exit code 1 if any day failed
26. The 10 mar 2026 source gap: 267 of 288 intervals in AEMO's own file
27. Config: 
    - The project ID comes from the environment (.env locally, workflow variables on Actions).
    - Everything else is in `config.py`.
    - paths use `Path(__file__)`, so it runs from any folder.
28. Logging: 
    - `basicConfig` only in `main.py`. 
    -  One line per day (rows + duration).
    -  A summary line
    - `logger.exception` for failures.
    - The retry warning comes before the pause.
## 5. Transformation
29. Staging = 2 views, one per raw table
30. AEMO's column names kept
31. `MARKET_DAY` = the date of the interval's start
32. Three findings:
    - RUNNO always 1
    - INTERVENTION always 0
    - time + region combinations are unique
33. Mart is a table rather than a view\
Reason: A view re-runs the query every time Looker reads it.
34. One mart for everything\
Reason: Looker Studio works best with a single data source. Joining several sources inside Looker is slow.
35. Summarise first, then full outer join\
Reason:
    - Summarise first: Joining raw rows matches each of a day's 288 price rows with all 288 demand rows, so every count is multiplied by 288. Summarising first means each side has exactly one row per day + region before the join.
    - Full outer join: If one table is missing a day or region, an inner join would drop that row completely. A full outer join keeps it, with NULLs on the missing side, so the gap is visible instead of hidden.
36. Count the RRP intervals above 300, above 5000 and below 0
    - Above 300: $300/MWh is the industry's standard cap-contract strike price. Above it, price-spike risk becomes real money.
    - Above 5000: This separates extreme spikes from ordinary ones.
    - Below 0: Negative prices mean oversupply, worth tracking.
37. Daily max `TOTALDEMAND` per region\
Reason: Peak demand stresses the grid and drives price spikes. It shows how high demand gets in the day.
38. The mart is rebuilt after each load\
Reason: The table does not update itself.
39. Hand Check: 2026-11-24, NSW1\
Method: Read (using parse.py) and calculated the numbers in pandas, from `PUBLIC_DISPATCHIS_20261124.zip`\
Result: `max_rrp`, `min_rrp`, `avg_rrp`, `rrp_intervals_above_300`, `rrp_intervals_above_5000`, `rrp_intervals_below_0`, `max_total_demand` all matched the mart.
## 6. Automation
40. run time is at 8:01AM everyday.\
Reason: newest NEMWEB files should already be published by then.
41. Timezone `Australia/Brisbane`\
Reason: Use Brisbane because Brisbane is UTC+10 year-round (no DST like Sydney)
