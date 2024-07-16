import requests

def get_ohlc(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/ohlc"
    headers = {"accept": "application/json",
               "x-cg-demo-api-key": "CG-V7svdvGGPNrMudeqx6c8jkPr"}

    params = {
        'vs_currency': 'usd',
        'days': '365'
    }

    response = requests.get(url, params=params, headers = headers)

    if response.status_code == 200:
        data = response.json()
        # response is list of lists with format: [timestamp, o, h, l, c]
        if not data:
            print("prices is empty")
    else:
        print(f'Error getting price data, code: {response.status_code}')
        return None
    return data

if __name__ == "__main__":
    get_ohlc("bitcoin")