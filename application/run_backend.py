import ml_utils
import requests
import pandas as pd
import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from datetime import datetime


def get_api():
    """Access the api and return the original dataframe."""
    global df_original
    global date
    headers = {
        'accept': 'application/json'
    }
    url = 'API-KEY-HERE'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.Timeout as errt:
        raise SystemExit(errt)
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit(errc)

    dataframes = []
    for i in range(1, json.loads(response.content)['paginas'] + 1):
        url = f'API-KEY-HERE'
        response = requests.get(url, headers=headers)
        dataframes.append(json.loads(response.content))

    datasets = []
    for item in dataframes:
        df = pd.DataFrame(item).T.iloc[:-4]
        datasets.append(df)

    df_original = pd.concat(item for item in datasets)
    df_original = df_original.loc[(df_original['Status'] == 'Aluguel') | (
        df_original['Status'] == 'Venda e Aluguel')]

    df_original['Mobiliado'] = df_original['Caracteristicas'].apply(
        lambda x: 2 if x['Mobiliado'] == 'Sim' else 1 if x['Semi Mobiliado'] == 'Sim' else 0)
    keys = df_original['Caracteristicas'].iloc[0].keys()
    df_original['Caracteristicas'] = df_original['Caracteristicas'].apply(
        lambda x: ", ".join([key for key in keys if x[key] == 'Sim']))

    df_original.loc[df_original['Categoria'] ==
                    'Salas/Conjuntos', 'Categoria'] = 'Sala'
    df_original.loc[df_original['Categoria'] ==
                    'Prédio Comercial', 'Categoria'] = 'Prédio'
    df_original.loc[df_original['Categoria'] ==
                    'Ponto Comercial', 'Categoria'] = 'Ponto'
    df_original.loc[df_original['Categoria'] ==
                    'Casa Em Condomínio', 'Categoria'] = 'Casa'

    residenciais = ['Apartamento', 'Kitnet', 'Casa', 'Cobertura']
    comerciais = ['Empreendimento', 'Sala', 'Galpão', 'Loja',
                  'Prédio', 'Ponto', 'Terreno', 'Box', 'Casa Comercial']

    df_original.loc[df_original['Categoria'].isin(
        residenciais), 'Finalidade'] = 'Residencial'
    df_original.loc[df_original['Categoria'].isin(
        comerciais), 'Finalidade'] = 'Comercial'

    date = datetime.now()
    return df_original, date


# create schedule in the background to atualize df and date
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=get_api,
    trigger=IntervalTrigger(minutes=15),
    id='df, date from get_api',
    name='Return dataframe, date every 15 minutes',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def get_predictions(id_, quantity_similar_items):
    """Return the df with the predictions with the API Key."""
    predictions, original_property = ml_utils.recommend(
        id_, df_original, quantity_similar_items)

    return (predictions, original_property, date)


def get_ids(quantidade):
    return df_original['Codigo'].values[0:quantidade]
