#import requests

#url = 'http://localhost:5000/api'
#r = requests.post(url,json={'SIZE': 7, 'DISTANCE': 190, 'DESIBEL': 86, 'AIRFLOW': 2.2, 'FREQUENCY':5})

#print(r.json())

import requests

url = 'http://localhost:5000/api'
data = {'SIZE': 7, 'DISTANCE': 190, 'DESIBEL': 86, 'AIRFLOW': 2.2, 'FREQUENCY':5}

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
