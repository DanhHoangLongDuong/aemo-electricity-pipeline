from google.cloud import bigquery
import pandas as pd
from parse import parse
from config import PROJECT_ID, BIGQUERY_DATASET
from decimal import Decimal
from pathlib import Path



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
        

def delete_rows(client, table_id, file_name):
    sql=f"""
        DELETE FROM `{table_id}`
        WHERE source_file = @file_name;
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("file_name", "STRING", file_name)
        ]
    )
    
    rows = client.query_and_wait(sql, job_config=job_config)
    
    return rows.num_dml_affected_rows


def load(path, column):
    client = bigquery.Client(project=PROJECT_ID)

    df = convert(path, column)
    
    table_id = (f"{PROJECT_ID}.{BIGQUERY_DATASET}.{table_name[column]}")

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        create_disposition=bigquery.CreateDisposition.CREATE_NEVER 
    )

    delete_rows_count = delete_rows(client, table_id, Path(path).name)
    
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    
    return delete_rows_count, job.output_rows



if __name__ == "__main__":
    print(load("../data/raw/PUBLIC_DISPATCHIS_20261115.zip", "REGIONSUM"))