#!/usr/bin/env python3

import requests
import json
import logging
import datetime

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

try:
    with open("data/lastseen.json", "r") as lsFile:
        lastseen = json.load(lsFile)
except:
    logging.critical("Last seen data missing")
    exit()

try:
    with open("data/members.json", "r") as lsFile:
        members = json.load(lsFile)
except:
    logging.critical("Member data missing")
    exit()

### Time Converstion Functions ###

# Time constands for headspace
hsFractal = 1 # done like this to allow for future adding for smaller units
hsSegmentLen = hsFractal * 6
hsDayLen = hsSegmentLen * 6
hsWeekLen = hsDayLen * 6
hsSeasonLen = hsWeekLen * 6
hsCycleLen = hsSeasonLen * 6

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

def rsSecondToFractal(rsSeconds):
    return(rsSeconds // 400)
            
### Headspace time date display ###
# a collection of ways to dispay headspace time

def hsTimeNow():
    timeFromZero = (datetime.datetime.now(datetime.UTC) - datetime.datetime.fromisoformat(zeropoint))

    hsNowObj = hsFractalTohsTimeObject(
            rsSecondToFractal(
                timeFromZero.total_seconds()
            )
        )

    return (hsNowObj)

def hsTimeShort(hsTimeObject):
    return (f"{hsTimeObject[0]:d}-{hsTimeObject[1]:d}-{hsTimeObject[2]:d}-{hsTimeObject[3]:d} {hsTimeObject[4]:d}:{hsTimeObject[5]:d}")

def hsTimeHuman(hsTimeObject):
    return (f"{hsTimeObject[0]:d} cycles, {hsTimeObject[1]:d} seasons, {hsTimeObject[2]:d} weeks, {hsTimeObject[3]:d} days, {hsTimeObject[4]:d} segments, {hsTimeObject[5]:d} fractals")

### Member last seen, total front time, and percent fronted ###

def rsLastSeen(member):
    rsTimeAgo = (datetime.datetime.now(datetime.UTC) - datetime.datetime.fromisoformat(lastseen[member]))
    return (rsTimeAgo)

def hsLastSeen(member):
    rsTimeAgo = rsLastSeen(member)
    hsTimeAgo = hsFractalTohsTimeObject(
            rsSecondToFractal(
                rsTimeAgo.total_seconds()
            )
        )
    return(hsTimeAgo)
