import requests

file = requests.get(f"https://nemweb.com.au/Reports/ARCHIVE/DispatchIS_Reports/PUBLIC_DISPATCHIS_20261112.zip")

if file:
    print(f"status code: {file.status_code}")
else:
    print(f"Error: {file.raise_for_status()}")
    