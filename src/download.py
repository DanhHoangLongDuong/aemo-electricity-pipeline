import requests
import time
from datetime import datetime
from pathlib import Path


def download(date):
    link_date = date.strftime("%Y%m%d")
    file_name = (f"PUBLIC_DISPATCHIS_{link_date}.zip")
    url = (f"https://nemweb.com.au/Reports/ARCHIVE/DispatchIS_Reports/{file_name}")
    path = Path(f"../data/raw/{file_name}")
    temp_path = Path(f"{path}.temp")
    
    if path.exists():
        print(f"file {file_name} already exists.")
    else:
        attempt = 0
        
        while True:
            try:
                file = requests.get(url, timeout=30)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                attempt += 1
                if attempt == 5:
                    raise
                time.sleep(3)
            else:     
                file.raise_for_status()
                break
        
        
        with open(temp_path, "wb") as zf:
            zf.write(file.content)
            
        temp_path.replace(path)
            
        
    return path

if __name__ == "__main__":
    dt = datetime.strptime("2026-11-13", "%Y-%m-%d")
    download(dt)
    
    
        