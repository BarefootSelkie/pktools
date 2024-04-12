#!/usr/bin/env python3

import logging
import yaml
import json
import os
import requests
import http.server
import socketserver

# Logging setup
logging.basicConfig(format="%(asctime)s : %(message)s", filename="pktserve.log", encoding='utf-8', level=logging.INFO)

# Load settings
try:
    with open("./config-pkts.yaml", "r") as read_file:
        config = yaml.safe_load(read_file)
except:
    logging.critical("Settings file missing")
    exit()

systemid = config["pluralkit"]["systemID"]
pktoken = config["pluralkit"]["token"]
zeropoint = config["pluralkit"]["zeropoint"]

### Data store building functions ###

# Get the raw system data from the PluralKit API and save it to disk
def buildPkSystem():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid, headers={'Authorization':pktoken})
        with open(os.path.expanduser(config["data"]) + "/pkSystem.json", "w") as systemFile:
            systemFile.write(r.text)
    except requests.exceptions.RequestException as e:
        logging.warning("Unable to fetch system data")
        logging.warning(e) 

# Get the raw data about system members from the PluralKit API and save it to disk
def buildPkMembers():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/members", headers={'Authorization':pktoken})
        with open(os.path.expanduser(config["data"]) + "/pkMembers.json", "w") as memberFile:
            memberFile.write(r.text)
    except requests.exceptions.RequestException as e:
        logging.warning("Unable to fetch member data")
        logging.warning(e) 

# Get the raw data about system groups from the PluralKit API and save it to disk
def buildPkGroups():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/groups?with_members=true", headers={'Authorization':pktoken})
        with open(os.path.expanduser(config["data"]) + "/pkGroups.json", "w") as groupsFile:
            groupsFile.write(r.text)
    except requests.exceptions.RequestException as e:
        logging.warning("Unable to fetch groups data")
        logging.warning(e)

# Get the raw data about the most recent switch from the PluralKit API and save it to disk
def buildLastSwitch():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/switches?limit=1", headers={'Authorization':pktoken})
        switches = r.json()
        with open(os.path.expanduser(config["data"]) + "/lastSwitch.json", "w") as outputFile:
            outputFile.write(json.dumps(switches[0]))
    except requests.exceptions.RequestException as e:
        logging.warning("Unable to fetch last switch data")
        logging.warning(e) 

### Main Code ###

if os.path.exists(os.path.expanduser(config["data"])):
    logging.info("Data store directory exists")
else:
    logging.info("Making data store directory")
    os.mkdir(os.path.expanduser(config["data"]))

### Discord message sending ###
# Used for notifiying of swtiches and also for server startup

def sendMessage(messageText, mode):
    logging.info("Sending Discord message")
    message = {"content": messageText}
    try:
        requests.post("https://discord.com/api/webhooks/" + config["discord"][mode]["serverID"] + "/" + config["discord"][mode]["token"], message)
    except requests.exceptions.RequestException as e:
        logging.warning("Unable to send message to discord")
        logging.warning(e) 

# On server startup fetch a fresh copy of the system from pluralkit
buildPkSystem()
buildPkMembers()
buildPkGroups()
buildLastSwitch()

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()