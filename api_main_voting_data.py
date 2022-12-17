import json
import requests
import pandas as pd
import pickle
from datetime import datetime, timezone

whole_data = []

for page in range(0,363):
    r = requests.get(
        f'https://avoindata.eduskunta.fi/api/v1/tables/SaliDBAanestys/rows'
        f'?page={page}'
        )

    if r.status_code != "200" and r.status_code != 200:
        print(r.status_code, r.content)
        break

    response_data = json.loads(r.content)

    columns = response_data["columnNames"]
    raw_data = response_data["rowData"]

    whole_data.insert(0, columns) if page == 1 else None

    whole_data.extend(raw_data)

data = pd.DataFrame(whole_data)

with open('data_main.json', 'w', encoding="UTF-8") as file:
    
    file.write(data.to_json())