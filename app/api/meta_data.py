import json
import requests

local_currency = 'USD'
local_symbol = '$'

api_key = 'd0fe3ffb-ff96-4162-abe2-08b6a1b4b770'
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'


symbol = 'tking'.upper()

meta_url = base_url + '/v1/cryptocurrency/info?&symbol=' + symbol

request = requests.get(meta_url, headers=headers)
results = request.json()
data = results['data']

name = data[symbol]['name']
desription = data[symbol]['description']
logo = data[symbol]['logo']
website = data[symbol]['urls']['website'][0]
twitter = data[symbol]['urls']['twitter'][0]
reddit = data[symbol]['urls']['reddit'][0]
white_paper = data[symbol]['urls']['technical_doc'][0]



print(name)
print(desription)
print(logo)
print(website)
print(twitter)