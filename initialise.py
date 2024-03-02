#!/usr/bin/env python3

# To be run if the files lastseen.json, members.json, and system.json are missing

import datetime
import json
import logging
import requests
import time

# Logging setup
logging.basicConfig(format="%(asctime)s : %(message)s", filename="pktools-init.log", encoding='utf-8', level=logging.INFO)

# Load settings from files and set settings varibles
try:
    with open("data/apikeys.json", "r") as read_file:
        pktsettings = json.load(read_file)
except:
    logging.critical("API Keys missing")
    exit()

systemid = pktsettings["pluralkit"]["systemID"]
pktoken = pktsettings["pluralkit"]["token"]
zeropoint = pktsettings["zeropoint"]

# create blank varibles
memberSeen = {}
pkMembers = {}

# Get the raw system data from the PluralKit API and save it to disk
def buildPkSystem():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid, headers={'Authorization':pktoken})
        with open("data/pkSystem.json", "w") as systemFile:
            systemFile.write(r.text)
    except requests.exceptions.RequestException as e:
        logging.warning("Unable to fetch system data")
        logging.warning(e) 

# Get the raw data about system members from the PluralKit API and save it to disk
def buildPkMembers():
    global pkMembers
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/members", headers={'Authorization':pktoken})
        pkMembers = r.json()
        with open("data/pkMembers.json", "w") as memberFile:
            memberFile.write(r.text)
    except requests.exceptions.RequestException as e:
        logging.warning("Unable to fetch member data")
        logging.warning(e) 

# Get the raw data about system groups from the PluralKit API and save it to disk
def buildPkGroups():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/groups?with_members=true", headers={'Authorization':pktoken})
        with open("data/pkGroups.json", "w") as groupsFile:
            groupsFile.write(r.text)
    except requests.exceptions.RequestException as e:
        logging.warning("Unable to fetch groups data")
        logging.warning(e) 


# Get the raw data about the most recent switch from the PluralKit API and save it to disk
def buildLastSwitch():
    try:
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/switches?limit=1", headers={'Authorization':pktoken})
        switches = r.json()
        with open("data/lastSwitch.json", "w") as outputFile:
            outputFile.write(json.dumps(switches[0]))
    except requests.exceptions.RequestException as e:
        logging.warning("Unable to fetch last switch data")
        logging.warning(e) 

# Given a batch of switches, updates the MemberSeen data
# Returns: timestamp of the oldest switch that was input
def updateMemberSeen(switches):
    global pkMembers
    global memberSeen

    # Switches are currently in reverse chronological order - make them in chronological order instead
    switches.reverse()

    previousSwitch = None
    for thisSwitch in switches:
        
        # Skip the first switch in a batch
        if previousSwitch is None:
            previousSwitch = thisSwitch
            continue

        for member in previousSwitch["members"]:
            if member not in thisSwitch["members"]:
                # A system member has left as of this switch
                if memberSeen[member]["lastOut"] < thisSwitch["timestamp"]:
                    memberSeen[member]["lastOut"] = thisSwitch["timestamp"]

        for member in thisSwitch["members"]:
            if member not in previousSwitch["members"]:
                # A system member has joined as of this switch
                if memberSeen[member]["lastIn"] < thisSwitch["timestamp"]:
                    memberSeen[member]["lastIn"] = thisSwitch["timestamp"]
        
        previousSwitch = thisSwitch

    # Return timestamp for the switch that we are up-to-date after
    return switches[1]["timestamp"]

# Pulls entire switch history from pluralkit and builds memberSeen from this
# useful for initial setup of data, in normal use would call PullPeriodic() instead
# This function writes the updated memberSeen to disk
# returns: eventually, can take several minutes to run
def buildMemberSeen():
    global pkMembers

    # Pluralkit requires us to request switches in batches of at most 100 a time
    # Keep track of where we have currently got up to
    pointer = datetime.datetime.now().isoformat(timespec="seconds") + "Z"

    # Initiailise the MemberSeen object so that we have an entry for all system members
    for member in pkMembers:  
        memberSeen[member["id"]] = {"lastIn": zeropoint, "lastOut": zeropoint}  

    # Keep requesting batches of switches from pluralkit
    while True:
        try:
            time.sleep(1) # flood protection
            logging.info("Getting switches before " + pointer)
            r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/switches?limit=100&before=" + pointer, headers={'Authorization':pktoken})
            switches = r.json()        
            # Stop if we've reached the very last switch
            if (len(switches) < 2): break
            # Otherwise, use the batch of data we just received to update MemberSeen
            pointer = updateMemberSeen(switches)
        except requests.exceptions.RequestException as e:
            # Fail silently
            logging.warning("Unable to fetch front history block " + pointer)
            logging.warning(e) 

    # Update the memberSeen file on the disk
    with open("data/memberSeen.json", "w") as output_file:
        output_file.write(json.dumps(memberSeen))

buildPkSystem()
buildPkMembers() 
buildPkGroups()     
buildLastSwitch()     
buildMemberSeen()