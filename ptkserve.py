#!/usr/bin/env python3

import logging
import yaml
import json
import os
import requests
import http.server
import socketserver
import socket
import threading
import time

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

# Web server setup

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.expanduser(config["data"]), **kwargs)
    def log_message(self, format, *args):
        return
    
def startWebServer():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

### Data store building functions ###

# Get the raw system data from the PluralKit API and save it to disk
def buildPkSystem():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid, headers={'Authorization':pktoken})
        with open(os.path.expanduser(config["data"]) + "/pkSystem.json", "w") as systemFile:
            systemFile.write(r.text)
    except Exception as e:
        logging.warning("PluralKit requests.get ( buildPkSystem )")
        logging.warning(e) 

# Get the raw data about system members from the PluralKit API and save it to disk
def buildPkMembers():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/members", headers={'Authorization':pktoken})
        with open(os.path.expanduser(config["data"]) + "/pkMembers.json", "w") as memberFile:
            memberFile.write(r.text)
    except Exception as e:
        logging.warning("PluralKit requests.get ( buildPkMembers )")
        logging.warning(e) 

# Get the raw data about system groups from the PluralKit API and save it to disk
def buildPkGroups():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/groups?with_members=true", headers={'Authorization':pktoken})
        with open(os.path.expanduser(config["data"]) + "/pkGroups.json", "w") as groupsFile:
            groupsFile.write(r.text)
    except Exception as e:
        logging.warning("PluralKit requests.get ( buildPkGroups )")
        logging.warning(e)

# Get the raw data about the most recent switch from the PluralKit API and save it to disk
def buildLastSwitch():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/switches?limit=1", headers={'Authorization':pktoken})
        switches = r.json()
        with open(os.path.expanduser(config["data"]) + "/lastSwitch.json", "w") as outputFile:
            outputFile.write(json.dumps(switches[0]))
    except Exception as e:
        logging.warning("PluralKit requests.get ( buildPkSwitch )")
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
        requests.post("https://discord.com/api/webhooks/" + str(config["discord"][mode]["serverID"]) + "/" + config["discord"][mode]["token"], message)
    except Exception as e:
        logging.warning("Discord error ( sendMessage )")
        logging.warning(e) 

# On server startup fetch a fresh copy of the system from pluralkit
buildPkSystem()
buildPkMembers()
buildPkGroups()
buildLastSwitch()

try:
    threading.Thread(target=startWebServer, daemon=True).start()
    hostname = socket.gethostname()
    ipAdr = socket.gethostbyname(hostname)
    message = "pktserve up\n" + "http://" + str(ipAdr) + ":" + str(PORT)
    sendMessage(message, "full")
except Exception as e:
        logging.warning("Web server error ( main )")
        logging.warning(e)

while True:
    time.sleep(10)
    print("running")