from ml_utils import *
import requests
import pandas as pd
import json

def get_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.Timeout as errt:
        raise SystemExit(errt)
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit(errc)

    conteudo = json.loads(response.content)
    df_original = pd.DataFrame(conteudo)
    df_original = df_original.loc[(df_original['contrato'] == 'Locação') | (df_original['contrato'] == 'Compra,Locação')]

    return df_original


def get_predictions(id_):

    conteudo = get_api("API-key here")

    predictions = recommend(id_, conteudo)

    return predictions


