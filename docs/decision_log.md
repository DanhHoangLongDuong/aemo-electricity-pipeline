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
10.(2026-11-15) `00:00` row belong to the previous day.
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
18. Skip if real file exists. Write to `.temp`, then rename
Reason: A crash never leaves a half file under the real name
19. Idempotency: Delete by `source_file`, then append.\
The `00:00` row lands in the next day's partition, hence partition repace is not used.
20. `source_file`: file name only (not the path), so it is the same wherever the code runs
21. Types converted in `load.py`, and `Decimal` for `NUMERIC`, never via `float`