#!/usr/bin/env python3

# To be run if the files lastseen.json, members.json, and system.json are missing

import time
import requests
import json
import logging
import os.path

# Logging setup
logging.basicConfig(format="%(asctime)s : %(message)s", filename="log.log", encoding='utf-8', level=logging.INFO)

# Load settings from files and set settings varibles
try:
    with open("data/apikeys.json", "r") as read_file:
        apikeys = json.load(read_file)
except:
    logging.critical("API Keys missing")
    exit()

systemid = apikeys["pluralkit"]["systemID"]
pktoken = apikeys["pluralkit"]["token"]

lastSeen = {}

def appendHistory(r, *args, **kwargs):
    logging.info("Appending history batch")
    data = r.json()
    if len(data) == 0:
        # nothing left - write out our results
        print(lastSeen)
        with open("data/lastseen.json", "w") as output_file:
            output_file.write(json.dumps(lastSeen))
        exit()

    # items have a members list and timestamp
    for item in data:
        for member in item["members"]:
            if member not in lastSeen:
                lastSeen[member] = item["timestamp"]

    # get the next batch
    fetchFrontHistory(data[len(data) - 1]["timestamp"])

def fetchFrontHistory(before):
    # Pause for one second so we don't hit rate limit
    time.sleep(1)
    print(before)
    logging.info("Fetching front history block " + before)
    try:
        requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/switches?limit=100&before=" + before, hooks={'response': appendHistory}, headers={'Authorization':pktoken})
    except requests.exceptions.RequestException as e:
        # Fail silently
        logging.warning("Unable to fetch front history block" + "1 - 100")
        logging.warning(e) 

# Using date far in future as too lazy to do datetime formmating right now    
fetchFrontHistory("2030-01-01T00:00:00Z")
    