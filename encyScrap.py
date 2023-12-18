import json
import requests
import time
from datetime import datetime


def getResourceEcyclopediaData(id: int) -> dict:
  url = f"https://www.simcompanies.com/api/v4/en/0/encyclopedia/resources/1/{id}/"
  # url = "https://jsonplaceholder.typicode.com/todos/1"
  print(f"Reaching ;{url}; for data.")
  headers = {'Accept': 'application/json'}
  response = requests.get(url, headers=headers, timeout=5)

  if response.status_code != 200:
    raise Exception("Error while fetching data from API")
  
  return response.json()

id = 101

data = getResourceEcyclopediaData(id)

now = datetime.now()
current_time = now.strftime("%d.%m.%Y_%H:%M")

filename = f'export/{id}_{data["name"]}_{current_time}.json'

with open(filename, "w") as outfile:
  json.dump(data, outfile)
