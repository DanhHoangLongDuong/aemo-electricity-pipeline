import requests
import time
import logging
from config import DATA_FOLDER, NEMWEB_URL, RETRY_ATTEMPT, TIMEOUT, PAUSE
from datetime import datetime



logger = logging.getLogger(__name__)

def download(date):
    link_date = date.strftime("%Y%m%d")
    file_name = (f"PUBLIC_DISPATCHIS_{link_date}.zip")
    url = (f"{NEMWEB_URL}{file_name}")
    path = DATA_FOLDER / file_name
    temp_path = path.with_suffix(path.suffix + ".temp")
    
    if path.exists():
        logger.info(f"file {file_name} already exists.")
    else:
        attempt = 0
        
        while True:
            try:
                file = requests.get(url, timeout=TIMEOUT)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                attempt += 1
                if attempt == RETRY_ATTEMPT:
                    raise
                
                logger.warning(f"Retry download file date {link_date}. Attempt: {attempt} of {RETRY_ATTEMPT}")
                time.sleep(PAUSE)
                
            else:
                file.raise_for_status()
                break
        
        
        with open(temp_path, "wb") as zf:
            zf.write(file.content)
            
        temp_path.replace(path)    
        logger.info(f"{link_date}: success. File size: {path.stat().st_size} bytes")
        
    return path



if __name__ == "__main__":
    dt = datetime.strptime("2026-11-13", "%Y-%m-%d")
    download(dt)
    
    
        