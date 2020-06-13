import requests
import json

main_link = 'https://api.github.com/users/mikhailseliverstov/repos'

response = requests.get(main_link)

data = response.json()

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
