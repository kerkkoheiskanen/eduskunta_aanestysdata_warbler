import json
import requests
import pandas as pd
import pickle
from datetime import datetime, timezone

whole_data = []

for page in range(0,1000000):
    r = requests.get(
        f'https://avoindata.eduskunta.fi/api/v1/tables/SaliDBAanestysJakauma/rows'
        f'?page={page}'
        )

    if r.status_code != "200" and r.status_code != 200:
        break

    response_data = json.loads(r.content)

    columns = response_data["columnNames"]
    raw_data = response_data["rowData"]

    whole_data.insert(0, columns) if page == 1 else None

    whole_data.extend(raw_data)

    if page % 5000 == 0:

        data = pd.DataFrame(whole_data)

        filename = "data_distr" + str(page)

        with open(filename + '.pkl', 'wb') as file:
            
            pickle.dump(data, file)

        with open(filename + '.json', 'w', encoding="UTF-8") as file:
            
            file.write(data.to_json())

data = pd.DataFrame(whole_data)

with open('data_distr.json', 'w', encoding="UTF-8") as file:
    
    file.write(data.to_json())