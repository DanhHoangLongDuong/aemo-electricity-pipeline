import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timezone, timedelta



load_dotenv()

PROJECT_ID = os.getenv("GCP_project")
if not PROJECT_ID:
    raise ValueError("GCP_project is not set. Add it to .env")

BIGQUERY_DATASET = "raw"
NEMWEB_URL = "https://nemweb.com.au/Reports/ARCHIVE/DispatchIS_Reports/"
MARKET_TZ = timezone(timedelta(hours=10))

RETRY_ATTEMPT = 5
TIMEOUT = 30
PAUSE = 3

DAY_LAG = 2
DAY_BACK = 365

TOP_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = TOP_FOLDER / "data" / "raw"