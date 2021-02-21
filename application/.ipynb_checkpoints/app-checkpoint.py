from run_backend import *
from ml_utils import *
from flask import Flask, request

app = Flask(__name__)

# def format_predictions(id_='73093'):
    
#     predictions = get_predictions(id_)

#     predictions_formatted = []

#     for i in predictions.iloc:
#         predictions_formatted.append(f"\
#         <tr><th><a>{i['codigo']}</a></th>\
#         <th>{i['subtipo']}</th>\
#         <th>{i['dormitorios']}</th>\
#         <th>{i['valor_locacao']}</th>\
#         <th>{i['endereco_bairro']}</th>\
#         </tr>")
#     return '\n'.join(predictions_formatted) #
    

@app.route('/')
def main_page():
    return f"""<head><h1>Recomendador de Imóveis da Órion</h1></head>
    <h3>Para utilizar, digite /predict?imovel_id="id_imovel"</h3>
    """ #

@app.route('/predict')
def predict_api():
    imovel_id = request.args.get("imovel_id", default=None)

    if imovel_id is None:
        return "not found"
    else:
        imovel_data = get_predictions(imovel_id)

    if imovel_data is None:
        return "not found"

    predictions_formatted = []

    for i in imovel_data.iloc:
        predictions_formatted.append(f"<tr><th><a>{i['codigo']}</a></th>\
        <th>{i['subtipo']}</th>\
        <th>{i['dormitorios']}</th>\
        <th>{i['valor_locacao']}</th>\
        <th>{i['endereco_bairro']}</th>\
        </tr>")
    preds = '\n'.join(predictions_formatted) #
    return f"""<head><h1>Recomendador de Imóveis da Órion</h1></head>
    <h2>Prevendo recomendações para o imóvel {imovel_id}</h2>
    <body>
    <table>
             {preds}
    </table>
    </body>""" #


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


