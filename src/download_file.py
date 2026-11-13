import requests


file = requests.get(f"https://nemweb.com.au/Reports/ARCHIVE/DispatchIS_Reports/PUBLIC_DISPATCHIS_20261112.zip", timeout=30)
    
print(f"status code: {file.status_code}")
print(f"file size: {len(file.content) / 1024 / 1024} MB")
    