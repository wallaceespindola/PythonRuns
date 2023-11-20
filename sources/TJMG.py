import requests
import json


def query_cnj_api(process_number):
    """
    Queries the CNJ API with the given process number and returns the response.

    :param process_number: The process number to query.
    :return: The response from the API.
    """
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
    }
    json_data = {
        "query": {
            "match": {
                "numeroProcesso": process_number
            }
        }
    }

    response = requests.post(url, json=json_data, headers=headers)
    return response.json()


# Example usage
print("####### Chamando public API TJMG - Proc Num, resultados no console...")
process_number = "13668284120218130024"
response = query_cnj_api(process_number)

# Pretty print the JSON response
pretty_json = json.dumps(response, indent=4)
print(pretty_json)
