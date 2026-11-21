import requests
import time
from config import DATA_FOLDER, NEMWEB_URL, RETRY_ATTEMPT, TIMEOUT, PAUSE
from datetime import datetime



def download(date):
    link_date = date.strftime("%Y%m%d")
    file_name = (f"PUBLIC_DISPATCHIS_{link_date}.zip")
    url = (f"{NEMWEB_URL}{file_name}")
    path = DATA_FOLDER / file_name
    temp_path = path.with_suffix(path.suffix + ".temp")
    
    if path.exists():
        print(f"file {file_name} already exists.")
    else:
        attempt = 0
        
        while True:
            try:
                file = requests.get(url, timeout=TIMEOUT)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                attempt += 1
                if attempt == RETRY_ATTEMPT:
                    raise
                time.sleep(PAUSE)
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
    
    
        