from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle
import os

colunas = ['tamanho','ano','garagem']

#serialização
modelo = pickle.load(open('..\\..\\models\\modelo.sva', 'rb'))

app = Flask(__name__)

#autenticação basica com basic_auth
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME') # pegando uma variavel de ambiente 
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

#import ipdb; ipdb.set_trace()

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return 'Minha primeira API. '

@app.route('/sentimento/<frase>')# <> receberá o valor da variável frase na própria rota, retornando um valor posteriormente.
@basic_auth.required # endpoint com autenticacao necessaria
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt_br', to='en')
    polaridade = tb_en.sentiment.polarity
    return "Polaridade {}".format(polaridade)

@app.route('/cotacao/', methods = ['POST'])#O input na variavel 'tamanho' precisa ser um 'inteiro'
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]# "for col in" sempre vai executar na sequencia "tamanho, ano e garagem" e dessa forma vai criando uma lista. 
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])# [0] para acessar o primeiro valor da array. Pois preco é uma array de um valor só. 

app.run(debug=True, host='0.0.0.0')