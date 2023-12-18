import configparser
from datetime import datetime
import json
import requests
import time


def getResourceEcyclopediaData(id: int) -> dict:
  url = f"https://www.simcompanies.com/api/v4/en/0/encyclopedia/resources/1/{id}/"
  # url = "https://jsonplaceholder.typicode.com/todos/1"
  print(f"Reaching ;{url}; for data.")
  headers = {'Accept': 'application/json'}
  response = requests.get(url, headers=headers, timeout=5)

  if response.status_code != 200:
    raise Exception("Error while fetching data from API")

  return response.json()


def readConfig(configFile: str) -> configparser.ConfigParser:
  config = configparser.ConfigParser()

  config.read(configFile)

  return config


def scrapSimcoEncyclopedia():
  config = readConfig("config.ini")

  if config.getboolean("encyclopediaScrap", "run") is False:
    print("Aborting simcoEnc scraping, config turned off")
    return

  id = int(config.get("encyclopediaScrap", "startID"))

  data = getResourceEcyclopediaData(id)

  data.update({"phase": "normal"})

  now = datetime.now()
  current_time = now.strftime("%d.%m.%Y_%H:%M")

  filename = f'export/{id}_{data["name"]}_{current_time}.json'

  with open(filename, "w") as outfile:
    json.dump(data, outfile)

  id += 1
  config.set("encyclopediaScrap", "startID", str(id))
  saveConfigFile(config)


def saveConfigFile(config: configparser.ConfigParser):
  with open("config.ini", "w") as configfile:
    config.write(configfile)


def regenConfigFile():
  config = configparser.ConfigParser()

  config.add_section("encyclopediaScrap")
  config.set("encyclopediaScrap", "startID", "1")
  config.set("encyclopediaScrap", "run", "True")
  config.set("encyclopediaScrap", "phase", "normal")
  with open("config.ini", "w") as configfile:
    config.write(configfile)


# MAIN FUNCTION HERE

if __name__ == "__main__":
  config = readConfig("config.ini")
  id = int(config.get("encyclopediaScrap", "startID"))
  while id <= 145:
    scrapSimcoEncyclopedia()
    time.sleep(300)
