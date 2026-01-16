import requests

def test_api():
    CURRENCY_PAIR = "USD-BRL"
    url = f"https://economia.awesomeapi.com.br/last/{CURRENCY_PAIR}"
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Dados recebidos: {data}")
        
        key = CURRENCY_PAIR.replace("-", "")
        if key in data:
            bid = data[key]["bid"]
            name = data[key]["name"]
            print(f"Sucesso! {name}: {bid}")
        else:
            print(f"Erro: Chave {key} não encontrada no JSON.")
    except Exception as e:
        print(f"Erro no teste: {e}")

if __name__ == "__main__":
    test_api()
