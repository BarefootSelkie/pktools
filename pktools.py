#!/usr/bin/env python3

import requests
import json
import logging
import datetime
import time

# Logging setup
logging.basicConfig(format="%(asctime)s : %(message)s", filename="pktools.log", encoding='utf-8', level=logging.INFO)

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

### Load in data stores and make globals from them ###

try:
    with open("data/memberSeen.json", "r") as lsFile:
        memberSeen = json.load(lsFile)
except:
    logging.critical("Last seen data missing")
    exit()

try:
    with open("data/pkMembers.json", "r") as lsFile:
        pkMembers = json.load(lsFile)
except:
    logging.critical("Member data missing")
    exit()

try:
    with open("data/pkSystem.json", "r") as lsFile:
        pkSystem = json.load(lsFile)
except:
    logging.critical("Member data missing")
    exit()

try:
    with open("data/pkGroups.json", "r") as lsFile:
        pkGroups = json.load(lsFile)
except:
    logging.critical("Group data missing")
    exit()

try:
    with open("data/lastSwitch.json", "r") as lsFile:
        lastSwitch = json.load(lsFile)
except:
    logging.critical("Last switch data missing")
    exit()

### Creation of data stores ###

# Given a batch of switches, updates the MemberSeen data
# Returns: timestamp of the oldest switch that was input
def updateMemberSeen(switches):
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



### Data access functions ###

# Return information about a particular system member
def getMember(memberID):
    return([i for i in pkMembers if i["id"] == memberID][0])

### Periodic data update functions ###

# Update information about current fronters and when they most recently switched in and out
# Returns: True if a switch has happened since last update, False otherwise
def pullPeriodic():

    global lastSwitch

    switchOccurred = False

    # Get data about the most recent switches
    try:
        logging.info("Getting most recent switches")
        r = requests.get("https://api.pluralkit.me/v2/systems/" + systemid + "/switches?limit=100", headers={'Authorization':pktoken})
        switches = r.json()

        if (len(switches) > 1):
            # 1) Check to see if a switch has occured
            if ("id" not in lastSwitch) or (switches[0]["id"] != lastSwitch["id"]):
                switchOccurred = True
                lastSwitch = switches[0]
                with open("data/lastSwitch.json", "w") as output_file:
                    output_file.write(json.dumps(lastSwitch))

                # 3) Update the information about when fronters were last seen      
                updateMemberSeen(switches)
                with open("data/memberSeen.json", "w") as output_file:
                    output_file.write(json.dumps(memberSeen))

    except requests.exceptions.RequestException as e:
        # Fail silently
        logging.warning("Unable to fetch recent switches")
        logging.warning(e) 

    return switchOccurred

### Time Converstion Functions ###

# Time constants for headspace
hsFractal = 1 # done like this to allow for future adding for smaller units
hsSegmentLen = hsFractal * 6
hsDayLen = hsSegmentLen * 6
hsWeekLen = hsDayLen * 6
hsSeasonLen = hsWeekLen * 6
hsCycleLen = hsSeasonLen * 6

# Converts an int of headspace fractals into a headspace date time object
# returns [cycles, seasons, weeks, days, segments, fractals]
def hsFractalTohsTimeObject(fractals):

    hsTimeObject = [0,0,0,0,0,0]
    # Time object is formatted Cycyle, Season, Week, Day, Segment, Fractal

    remainder = fractals
    hsTimeObject[0] = int(fractals // hsCycleLen)
    remainder = fractals % hsCycleLen
    hsTimeObject[1] = int(remainder // hsSeasonLen)
    remainder = fractals % hsSeasonLen
    hsTimeObject[2] = int(remainder // hsWeekLen)
    remainder = fractals % hsWeekLen
    hsTimeObject[3] = int(remainder // hsDayLen)
    remainder = fractals % hsDayLen
    hsTimeObject[4] = int(remainder // hsSegmentLen)
    remainder = fractals % hsSegmentLen
    hsTimeObject[5] = int(remainder // hsFractal)

    return(hsTimeObject)

# Takes in a period of time in seconds and converts it to a number of headspace fractals
# Designed to work with *datetime.total_seconds()*, returns an int
def rsSecondToFractal(rsSeconds):
    return(rsSeconds // 400)
            
### Headspace time date display ###
# a collection of ways to dispay headspace time

# Convert a pluralkit string representing a datetime to a python datetime object
# Returns: python datetime object
def toPythonDateTime(input):
    # TODO: this is horribly hacky way of translating the date
    # This is needed purely for supporting RPis with python 3.9 installed
    # This version of python does not understand pluralkit's datetimes
    # as they do not follow the exact format it is expecting
    # Python 3.11 onwards does not have this issue
    return datetime.datetime.fromisoformat(input[0:19])

# Gets the current time in headspace based on zeropoint in apikeys.json
# returns: [cycles, seasons, weeks, days, segments, fractals]
def hsTimeNow():
    timeFromZero = (datetime.datetime.utcnow() - toPythonDateTime(zeropoint))

    hsNowObj = hsFractalTohsTimeObject(
            rsSecondToFractal(
                timeFromZero.total_seconds()
            )
        )

    return (hsNowObj)

# Convert a headspace time to a string 
# Returns: time in the format "x-x-x-x x:x"
def hsTimeShort(hsTimeObject):
    return (f"{hsTimeObject[0]:d}-{hsTimeObject[1]:d}-{hsTimeObject[2]:d}-{hsTimeObject[3]:d} {hsTimeObject[4]:d}:{hsTimeObject[5]:d}")

# Convert a headspace time to a string
# Returns: time in the format "x cycles, x seasons, x weeks, x days, x segments, x fractals"
def hsTimeHuman(hsTimeObject):
    return (f"{hsTimeObject[0]:d} cycles, {hsTimeObject[1]:d} seasons, {hsTimeObject[2]:d} weeks, {hsTimeObject[3]:d} days, {hsTimeObject[4]:d} segments, {hsTimeObject[5]:d} fractals")

### Member last seen, total front time, and percent fronted ###

# Get realsapce time elapsed since a memnber last started fronting
# Returns: integer of realspace seconds since the member started fronting
def rsSinceLastIn(member):
    return (datetime.datetime.utcnow() - toPythonDateTime(memberSeen[member]["lastIn"]))

# Get headspace time elapsed since a member last started fronting
# Returns: integer of headspace fractals since the member started fronting
def hsSinceLastIn(member):
    rsTimeAgo = rsSinceLastIn(member)
    hsTimeAgo = hsFractalTohsTimeObject(
            rsSecondToFractal(
                rsTimeAgo.total_seconds()
            )
        )
    return(hsTimeAgo)

# Get realsapce time elapsed since a member last stopped fronting
# Returns: integer of realspace seconds since the member stopped fronting
def rsLastSeen(member):
    rsTimeAgo = (datetime.datetime.utcnow() - toPythonDateTime(memberSeen[member]["lastOut"]))
    return (rsTimeAgo)

# Get headspace time elapsed since a member last stopped fronting
# Returns: integer of headspace fractals since the member stopped fronting
def hsLastSeen(member):
    rsTimeAgo = rsLastSeen(member)
    hsTimeAgo = hsFractalTohsTimeObject(
            rsSecondToFractal(
                rsTimeAgo.total_seconds()
            )
        )
    return(hsTimeAgo)
