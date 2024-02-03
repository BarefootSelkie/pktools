# pk-timetools
A set of useful tools that run on a rasberry pi to handle automatic switching out, displaying who's fronting, and tracking time since fronted.

## Setup

### apikeys.json example
``{
    "pluralkit": 
    {   
        "token": "",
        "systemID": ""
    },
    "discord":
    {
        "token": "",
        "serverID": "",
        "userID": ""
    }
}``

### Cron job for switchout.py

``0 0 * * * cd /home/pi && python3 ./switchout.py``

## Implimented functions

**rsSecondToFractal(rsSeconds)** takes in a period of time in seconds and converts it to a number of headspace fractals, designed to work with *datetime.total_seconds()*, returns an int

**hsFractalTohsTimeObject(hsFractals)** converts an int of headspace fractals into a headspace date time object, returns [cycles, seasons, weeks, days, segments, fractals]

**hsTimeNow()** gets the current time in headspace based on zeropoint in apikeys.json, returns [cycles, seasons, weeks, days, segments, fractals]

hsTimeShort(hsTimeObject)

hsTimeHuman(hsTimeObject)

rsLastSeen(member)

hsLastSeen(member)

## Missing functions

pullPeriodic - peridoically check to see if the current fronting member has changed and update lastseen.json ( only checks the last 6 switches )

pullBackUp - fetches the system and member objects from the server, ideally run daily

### Maybe not implementable if using a microcontroller with a small amount of memory:

allTime(member) - if member is included returns their total fronting time, if no member provided returns a list of all members and each of their total fronting time

allPercent(member) - returns a list of all members and their percentage of fronting

recientTime(member) - returns the amount of time that a member has fronted for in the last cycle

recientPercent(member) - returns the percentage of time a member has been fronting for in the last cycle