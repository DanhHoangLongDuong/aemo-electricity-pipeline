import sys
import time
from download import download
from load import load
from config import PROJECT_ID, DAY_BACK, DAY_LAG, BIGQUERY_DATASET, MARKET_TZ, PAUSE
from google.cloud import bigquery
from datetime import datetime, timedelta



def bigquery_table_check(project_id, table):
    sql=f"""
        SELECT source_file
        FROM `{project_id}.{BIGQUERY_DATASET}.{table}`
        GROUP BY source_file
    """

    client = bigquery.Client(project=project_id)
    rows = client.query_and_wait(sql)

    added_date = []
    for row in rows:
        raw_value = row["source_file"].removeprefix("PUBLIC_DISPATCHIS_").removesuffix(".zip")
        value = datetime.strptime(raw_value, "%Y%m%d").date()
        added_date.append(value)

    return added_date

price_table_date = bigquery_table_check(PROJECT_ID, "price")
region_sum_table_date = bigquery_table_check(PROJECT_ID, "region_sum")

common_date = set(price_table_date).intersection(set(region_sum_table_date))

day_list = []
today = datetime.now(MARKET_TZ).date()
for i in range(DAY_LAG, DAY_BACK + DAY_LAG):
    download_date = today - timedelta(days=i)
    day_list.append(download_date)


missing_days = sorted(list(set(day_list) - set(common_date)))



failed = []
for day in missing_days:
    
    try:
        path = download(day)
        price_value = load(path, "PRICE")
        region_sum_value = load(path, "REGIONSUM")
        
        print(f"{day}: price {price_value}, region_sum {region_sum_value}")
        time.sleep(PAUSE)
    except Exception as e:
        print(f"{day} failed: {e}")
        failed.append(day)
    
if failed:
    sys.exit(failed)