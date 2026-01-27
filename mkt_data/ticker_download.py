import json
import requests
import pandas as pd

def get_tickers(call_API = False,url = None, key = None, file_name = None, exchange_name="NASDAQ"):
    if call_API : return api_call(url, key, exchange_name)
    else:
        file = open(file_name).read()
        data = pd.DataFrame(json.loads(file))
        return data


def api_call(url, key, exchange_name="NASDAQ"):
    url = f"{url}{exchange_name}?token={key}"
    call = requests.get(url).text
    data = pd.DataFrame(json.loads(call))
    return data