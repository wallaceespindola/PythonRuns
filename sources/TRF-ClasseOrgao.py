import json

import requests

print("####### Calling public TRF API by Class/Org and showing output in the console...")

url = "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search"

payload = json.dumps({
    "query": {
        "bool": {
            "must": [
                {"match": {"classe.codigo": 1116}},
                {"match": {"orgaoJulgador.codigo": 13597}}
            ]
        }
    }
})

headers = {
    'Authorization': 'ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    # 'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
