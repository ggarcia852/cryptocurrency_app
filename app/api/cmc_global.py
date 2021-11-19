import json
import requests

local_currency = 'USD'
local_symbol = '$'

api_key = 'd0fe3ffb-ff96-4162-abe2-08b6a1b4b770'
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

global_url = base_url + '/v1/global-metrics/quotes/latest?convert=' + local_currency

request = requests.get(global_url, headers=headers)
results = request.json()

print(json.dumps(results, sort_keys=True, indent=4))

data = results['data']

active = data['active_cryptocurrencies']

total_market_cap = data['quote'][local_currency]['total_market_cap']

eth_dom = data['eth_dominance']

total_vol_24hr = data['quote'][local_currency]['total_volume_24h']

total_market_cap = round(total_market_cap, 2)
total_vol_24hr = round(total_vol_24hr, 2)

total_market_cap_string = local_symbol + '{:,}'.format(total_market_cap)
total_vol_24hr_string = local_symbol + '{:,}'.format(total_vol_24hr)


print(active, total_market_cap_string, total_vol_24hr_string)
