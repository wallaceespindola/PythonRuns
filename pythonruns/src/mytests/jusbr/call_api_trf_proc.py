import json
import os
import sys

import requests

print("####### Calling public TRF API by Num Proc and showing output in the console...")

url = "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search"

payload = json.dumps({"query": {"match": {"numeroProcesso": "00008323520184013202"}}})

# Public key published by CNJ at https://datajud-wiki.cnj.jus.br/api-publica/acesso (rotates occasionally).
api_key = os.environ.get("DATAJUD_API_KEY")
if not api_key:
    sys.exit("Set DATAJUD_API_KEY (see .env.example) to call the DataJud public API.")

headers = {
    "Authorization": f"APIKey {api_key}",
    "Content-Type": "application/json",
}

response = requests.request("POST", url, headers=headers, data=payload).json()

# Pretty print the JSON response
pretty_json = json.dumps(response, indent=4)
print(pretty_json)
