import requests

url = 'http://127.0.0.1:5000/cotacao/'

dados = {
    "tamanho":180,
    "ano":2010,
    "garagem":5
}

auth = requests.auth.HTTPBasicAuth('ramiro','alura')

response = requests.post(url, json=dados,auth=auth)
response.json()
