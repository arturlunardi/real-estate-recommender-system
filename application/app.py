import run_backend
from flask import Flask, request, render_template, url_for, redirect
import os
from datetime import datetime

os.chdir(os.path.abspath(os.path.dirname(__file__)))

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        # Get the first x id's to show on the main page
        ids = run_backend.get_ids(10)
        return render_template('index.html', ids=ids)
    else:
        # redirect for /predict - button
        return redirect(url_for("predict_api",
                                imovel_id=request.form.get('predict')))


@app.route('/predict', methods=['GET', 'POST'])
def predict_api():
    if request.method == 'GET':
        imovel_id = request.args.get("imovel_id", default=None)
    else:
        # redirect for /predict - button
        return redirect(url_for("predict_api",
                                imovel_id=request.form.get('predict')))
    if imovel_id is None:
        return render_template('404.html')
    else:
        # run the predictions and return the y similar items.
        imovel_data, original_property, date = run_backend.get_predictions(
            id_=imovel_id, quantity_similar_items=5)
    if imovel_data is None:
        return render_template('404.html')
    last_update = abs(datetime.now()-date).seconds / 60
    return render_template('recomendations.html',
                           df_dict=imovel_data,
                           original_property=original_property,
                           last_update=last_update)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
