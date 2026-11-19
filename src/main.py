import sys
import time
from download import download
from load import load
from datetime import datetime, timedelta, timezone


failed = []
today = datetime.now(timezone(timedelta(hours=10))).date()

for i in range(2, 5):
    download_date = today - timedelta(days=i)
    
    try:
        path = download(download_date)
        price_value = load(path, "PRICE")
        region_sum_value = load(path, "REGIONSUM")
        
        print(f"{download_date}: price {price_value}, region_sum {region_sum_value}")
        time.sleep(3)
    except Exception as e:
        print(f"{download_date} failed: {e}")
        failed.append(download_date)
    
if failed:
    sys.exit(failed)