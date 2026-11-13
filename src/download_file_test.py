import requests


file = requests.get(f"https://nemweb.com.au/Reports/ARCHIVE/DispatchIS_Reports/PUBLIC_DISPATCHIS_20261112.zip", timeout=30)

file.raise_for_status()
print(f"status code: {file.status_code}")
print(f"file size: {round((len(file.content) / 1024 / 1024), 2)} MB")
    