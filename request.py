import requests

url = 'http://localhost:5000/api'
data = {'Idade': 0, 'Sexo': 1, 'ETNIA': 0,
        'ESTADO_CIVIL': 1, 'I.R.A.': 0,
        'FORMA_INGRESSO': 0,
        'Tipo_Escola_Origem': 0}

response = requests.post(url, json=data)

# Verifique se a resposta foi bem-sucedida (código de status 200)
if response.status_code == 200:
    try:
        # Tente decodificar o JSON
        result = response.json()
        print(result)
    except requests.exceptions.JSONDecodeError as e:
        print("Erro ao decodificar JSON:", e)
else:
    print("Erro na solicitação. Código de status:", response.status_code)
