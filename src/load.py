import os
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas as pd
from parse import parse
from decimal import Decimal
from pathlib import Path


load_dotenv()

table_name = {
    "PRICE":"price",
    "REGIONSUM":"region_sum"
}

def convert(path, column):
    table = parse(path, column)
    
    
    table = table.astype({
        "RUNNO": "int64",
        "INTERVENTION": "int64"
    })
    
    table["SETTLEMENTDATE"] = pd.to_datetime(table["SETTLEMENTDATE"], format="%Y/%m/%d %H:%M:%S")
    table["source_file"] = Path(path).name
    
    if column == "PRICE":
        table["LASTCHANGED"] = pd.to_datetime(table["LASTCHANGED"], format="%Y/%m/%d %H:%M:%S")
        table["RRP"] = table["RRP"].map(Decimal)
    
    elif column == "REGIONSUM":
        table["TOTALDEMAND"] = table["TOTALDEMAND"].map(Decimal)
    
    
    return table
        
        
def load(path, column):
    project_id = os.getenv("GCP_project")
    if not project_id:
        raise ValueError("GCP_project is not set. Add it to .env")

    client = bigquery.Client(project=project_id)

    df = convert(path, column)
    
    table_id = (f"{project_id}.raw.{table_name[column]}")

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        create_disposition=bigquery.CreateDisposition.CREATE_NEVER 
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    
    return job.result()



if __name__ == "__main__":
    print(load("../data/raw/PUBLIC_DISPATCHIS_20261115.zip", "PRICE"))