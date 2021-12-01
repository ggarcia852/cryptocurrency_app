import json
import requests

local_currency = 'USD'
local_symbol = '$'

api_key = 'd0fe3ffb-ff96-4162-abe2-08b6a1b4b770'
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

gainers_url = base_url + '/v1/cryptocurrency/trending/gainers-losers'

request = requests.get(gainers_url, headers=headers)
results = request.json()

print(json.dumps(results, sort_keys=True, indent=4))