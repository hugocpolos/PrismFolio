import requests
import os


def get_current_stock_price(stock_code):
    url = "https://brapi.dev/api/quote/{}".format(stock_code.upper())
    params = {
        'token': os.getenv('STOCK_API_KEY'),
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise requests.HTTPError(f"Request failed with status code {response.status_code}."
                                 f"\n\t{response.json()}")

    data = response.json()
    return data.get('results')[0].get('regularMarketPrice')


def get_price_earning(stock_code):
    url = "https://brapi.dev/api/quote/{}".format(stock_code.upper())
    params = {
        'token': os.getenv('STOCK_API_KEY'),
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise requests.HTTPError(f"Request failed with status code {response.status_code}."
                                 f"\n\t{response.json()}")

    data = response.json()
    return data.get('results')[0].get('priceEarnings')
