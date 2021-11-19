import json
import requests

local_currency = 'USD'
local_symbol = '$'

api_key = 'd0fe3ffb-ff96-4162-abe2-08b6a1b4b770'
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

symbol = 'tking'.upper()

global_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol

request = requests.get(global_url, headers=headers)
results = request.json()

# print(json.dumps(results, sort_keys=True, indent=4))

data = results['data']
coin = data[symbol]
name = coin['name']

price = coin['quote'][local_currency]['price']
percent_change_24hr = coin['quote'][local_currency]['percent_change_24h']
market_cap = coin['quote'][local_currency]['market_cap']

price = round(price, 6)
percent_change_24hr = round(percent_change_24hr, 2)
market_cap = round(market_cap, 2)

price_string = local_currency + ' {:,}'.format(price)
percent_change_24hr_string = local_currency + ' {:,}'.format(percent_change_24hr)
market_cap_string = local_currency + ' {:,}'.format(market_cap)

print(name + '(' + symbol + ')')
print('Price: ' + price_string)
print('24hr Change: ' + percent_change_24hr_string)
print('Market Cap: ' + market_cap_string)
print()