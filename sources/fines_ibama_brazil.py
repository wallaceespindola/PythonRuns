# REFERENCE URL: 'http://dadosabertos.ibama.gov.br/dados/SICAFI/AC/Quantidade/multasDistribuidasBensTutelados.json'

import locale

import pandas as pd
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Locale PT BR - R$
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


def get_states():
    return [
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    ]


def main():
    print("IBAMA Brazil - Accessing environmental fines list...")

    print("\n>>> OPTIONS:")
    for code, name in get_states():
        print(f"{code} - {name}")

    while True:
        typed_state = input("\n>>> ENTER YOUR OPTION: ").upper()
        if any(code == typed_state for code, name in get_states()):
            state = typed_state
            state_name = next(name for code, name in get_states() if code == typed_state)
            break
        else:
            print("Invalid option. Please type a valid state acronym.")

    print(f"\n### Fetching data for: {state} - {state_name}...")

    response = requests.get(
        f"http://dadosabertos.ibama.gov.br/dados/SICAFI/{state}/Quantidade/multasDistribuidasBensTutelados.json",
        verify=False,  # No SSL verification
    )

    if response.status_code == 200:
        list_of_process = response.json()
        amount = len(list_of_process["data"])
        print(f"\n>>> {amount} processes found")
        categories = ["Fauna", "Flora", "Pesca", "Controle ambiental", "Outras"]

        for category in categories:
            print(f"\nAccessing fines about {category} ...")
            filtered_processes = [process for process in list_of_process["data"] if process["tipoInfracao"] == category]

            # Uncomment to see the data
            # print(f'\nProcesses for category {category}: \n{filtered_processes}\n')

            count = len(filtered_processes)
            print(f"{count} fines related to {category} found!")

            row = {
                "municipio": [process["municipio"] for process in filtered_processes],
                "nomeRazaoSocial": [process["nomeRazaoSocial"] for process in filtered_processes],
                "valorAuto": [
                    locale.currency(process["valorAuto"], grouping=True, symbol=True) for process in filtered_processes
                ],
                "dataAuto": [process["dataAuto"] for process in filtered_processes],
                "situacaoDebito": [process["situacaoDebito"] for process in filtered_processes],
                "enquadramentoLegal": [process["enquadramentoLegal"] for process in filtered_processes],
            }

            df = pd.DataFrame(row)
            output_file = f"../output/{category}.csv"
            df.to_csv(output_file, index=True, index_label="ID")
            print(f"Fines related to {category} have been saved to CSV file: [{output_file}].")
    else:
        print(f"REQUEST ERROR - RESPONSE CODE: [{response.status_code}]")

    print("\nIBAMA Brazil - search completed.")


if __name__ == "__main__":
    main()
