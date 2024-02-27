import recomendacao_apriori
from flask import Flask, request, jsonify

#buyer = "'0015f00000jkOhoAAE'"
#produtos_recomendados = recomendacao_apriori.main(buyer)
#print(produtos_recomendados)


app = Flask(__name__)

@app.route('/recommendation', methods=['POST'])
def recommendation():
    buyer = request.json.get('buyer')  # Obtém o valor de 'buyer' do corpo da requisição JSON
    output = recomendacao_apriori.main(buyer)  # Chama a função main() com o valor de 'buyer'
    return output  # Retorna o output como uma resposta JSON

if __name__ == '__main__':
    app.run(debug=True)
