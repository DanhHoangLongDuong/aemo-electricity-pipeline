import io
import csv
import zipfile
import pandas as pd

column_dict = {
    "PRICE": ["SETTLEMENTDATE", "REGIONID", "RUNNO", "INTERVENTION", "RRP", "PRICE_STATUS", "LASTCHANGED"],
    "REGIONSUM": ["SETTLEMENTDATE", "REGIONID", "RUNNO", "INTERVENTION", "TOTALDEMAND"]
}

def parse(path, column):
    header = None
    data = []

    if column not in column_dict:
        raise ValueError("column not in dictionary")
    
    with zipfile.ZipFile(path, 'r') as outer_zip:
        for sub_zipfile in outer_zip.namelist():
            with outer_zip.open(sub_zipfile) as inner_file:
                with zipfile.ZipFile(inner_file, "r") as inner_zip:
                    for file in inner_zip.namelist():
                        with inner_zip.open(file, "r") as binary_file:
                            text_file = io.TextIOWrapper(binary_file, encoding="utf-8")
                            for row in csv.reader(text_file):
                                if row[1] == "DISPATCH" and row[2] == column:
                                    if row[0] == "I":
                                        if header is None:
                                            header = row
                                    else:
                                        data.append(row)

    df = pd.DataFrame(data, columns=header)
    return df[column_dict[column]]
        
        
        
if __name__ == "__main__":
    print(parse("../data/raw/PUBLIC_DISPATCHIS_20261115.zip", "PRICE"))