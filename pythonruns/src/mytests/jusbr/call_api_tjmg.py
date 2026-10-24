import json
import os
import sys

import requests

# Public key published by CNJ at https://datajud-wiki.cnj.jus.br/api-publica/acesso (rotates occasionally).
api_key = os.environ.get("DATAJUD_API_KEY")
if not api_key:
    sys.exit("Set DATAJUD_API_KEY (see .env.example) to call the DataJud public API.")


def query_cnj_api(process_number):
    """
    Queries the CNJ API with the given process number and returns the response.

    :param process_number: The process number to query.
    :return: The response from the API.
    """
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"APIKey {api_key}",
    }
    json_data = {"query": {"match": {"numeroProcesso": process_number}}}

    response = requests.post(url, json=json_data, headers=headers, timeout=30)
    return response.json()


# Example usage
print("####### Chamando public API TJMG - Proc Num, resultados no console...")
process_number = "13668284120218130024"
response = query_cnj_api(process_number)

# Pretty print the JSON response
pretty_json = json.dumps(response, indent=4)
print(pretty_json)
