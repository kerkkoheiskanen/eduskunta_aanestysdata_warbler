import json
import requests
import pandas as pd
from datetime import datetime, timezone

def get_data():

    r = requests.get(
        f'https://avoindata.eduskunta.fi/api/v1/tables/SaliDBIstunto/rows'
        #f'/range?vs_currency=eur&from={ts_startdate}&to={ts_enddate}'
        )

    response_data = json.loads(r.content)

    print(response_data.keys())

    data = pd.DataFrame.from_dict(response_data, orient='index')

    raise Exception(data.info())
    

    return result_data
