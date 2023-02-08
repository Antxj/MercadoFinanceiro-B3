import requests
import pandas as pd


def get_agro():

    session = requests.session()
    session.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "accept": "application/json ..."
    })

    url = "https://investidor10.com.br/api/fiagro/comparador-mesmo-segmento/table/33/"

    response = session.get(url)
    data = response.json()["data"]

    df = pd.DataFrame(data)
    df.to_csv("agro.csv")


get_agro()
