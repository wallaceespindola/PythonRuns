import json

import requests

print("####### Calling public TRF API by Num Proc and showing output in the console...")

url = "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search"

payload = json.dumps({"query": {"match": {"numeroProcesso": "00008323520184013202"}}})

headers = {
    "Authorization": "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==",
    # 'ApiKey': 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    # 'appid': 'ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    # 'appid': 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    "Content-Type": "application/json",
}

response = requests.request("POST", url, headers=headers, data=payload).json()

# Pretty print the JSON response
pretty_json = json.dumps(response, indent=4)
print(pretty_json)
