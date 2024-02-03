#!/usr/bin/env python3

import requests
import json
import logging
import datetime
import pktools 

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

with open("data/lastseen.json", "r") as lsFile:
    lastseen = json.load(lsFile)

with open("data/members.json", "r") as lsFile:
    members = json.load(lsFile)

print("Current time : " + pktools.hsTimeHuman(pktools.hsTimeNow()) + "\n")

for member in lastseen:
    who = [i for i in members if i["id"] == member][0]["name"]

    print(str(who) + ": " + str(pktools.rsLastSeen(member)) + " = " + pktools.hsTimeShort(pktools.hsLastSeen(member)))
    