#!/usr/bin/env python3

import time
import requests
import json
import logging
import os.path

# Logging setup
logging.basicConfig(format="%(asctime)s : %(message)s", filename="log.log", encoding='utf-8', level=logging.INFO)

# Define and clear varibles
apikeys = 0
pktoken = 0

# Load settings from files and set settings varibles
with open("data/apikeys.json", "r") as read_file:
    apikeys = json.load(read_file)

systemid = apikeys["pluralkit"]["systemID"]
pktoken = apikeys["pluralkit"]["token"]

def writeSystem(r, *args, **kwargs):
    logging.info("Fetched system; checking for updates")
    
    # If file exists and is up to date stop the function
    if os.path.isfile("data/system.json"):
        with open("data/system.json", "r") as read_file:
            localSystem = read_file.read()
            if localSystem == r.content:
                logging.info("System headder unchanged")
                return
            
    logging.info("System header changed; updating local copy")
    # Otherwise overwrite the file with the new data from pluralkit
    with open("data/system.json", "w") as systemFile:
        systemFile.write(r.text)

def writeMembers(r, *args, **kwargs):
    logging.info("Fetched members; checking for updates")
    
    # If file exists and is up to date stop the function
    if os.path.isfile("data/members.json"):
        with open("data/members.json", "r") as read_file:
            localMembers = read_file.read()
            if localMembers == r.content:
                logging.info("Member list unchanged")
                return
    
    logging.info("Member list changed; updating local copy")
    # Otherwise overwrite the file with the new data from pluralkit
    with open("data/members.json", "w") as membersFile:
        membersFile.write(r.text)

def fetchFullSystem():
    logging.info("Starting fetch")
    try:
        requests.get("https://api.pluralkit.me/v2/systems/" + systemid, hooks={'response': writeSystem}, headers={'Authorization':pktoken})
    except requests.exceptions.RequestException as e:
        # Fail silently
        logging.warning("Unable to fetch system header")
        logging.warning(e) 
    
    # Pause for one second so we don't hit rate limit
    time.sleep(1)
    
    # Fetch the member list
    try:
        requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/members", hooks={'response': writeMembers}, headers={'Authorization':pktoken})
    except requests.exceptions.RequestException as e:
        # Fail silently
        logging.warning("Unable to fetch members")
        logging.warning(e) 

fetchFullSystem()