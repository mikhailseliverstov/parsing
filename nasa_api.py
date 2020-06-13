import requests
import json

main_link = 'https://api.nasa.gov/neo/rest/v1/feed?start_date=2020-06-08&end_date=2020-06-12&api_key=JjfGiEV2r9lTHzoBkSG1hexHMQiz9YaiccDRxqnY'

response = requests.get(main_link)

data = response.json()

print(data)