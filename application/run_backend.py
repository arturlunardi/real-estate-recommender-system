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
    url = "API-key here"
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

    content = json.loads(response.content)
    df_original = pd.DataFrame(content)
    df_original = df_original.loc[(df_original['contrato'] == 'Locação') | (
        df_original['contrato'] == 'Compra,Locação')]
    date = datetime.now()
    return df_original, date


content = get_api()

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
    return df_original['codigo'].values[0:quantidade]
