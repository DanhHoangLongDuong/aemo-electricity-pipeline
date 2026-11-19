import os
import sys
import time
from download import download
from load import load
from dotenv import load_dotenv
from google.cloud import bigquery
from datetime import datetime, timedelta, timezone


load_dotenv()
project_id = os.getenv("GCP_project")

def bigquery_table_check(project_id, table):
    sql=f"""
        SELECT source_file
        FROM `{project_id}.raw.{table}`
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

price_table_date = bigquery_table_check(project_id, "price")
region_sum_table_date = bigquery_table_check(project_id, "region_sum")

common_date = set(price_table_date).intersection(set(region_sum_table_date))

day_list = []
today = datetime.now(timezone(timedelta(hours=10))).date()
for i in range(2, 367):
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
        time.sleep(3)
    except Exception as e:
        print(f"{day} failed: {e}")
        failed.append(day)
    
if failed:
    sys.exit(failed)