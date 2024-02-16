# pktools
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

## Data files

pkSwitches - backup of all switches pulled from PluralKit
pkMembers - full list of system members and information about these members pulled from PluralKit - see https://pluralkit.me/api/models/
pkSystem - data pulled from PluralKit about the system itself (e.g. system name) - see https://pluralkit.me/api/models/
memberStats - dictionary from shortCode to lastIn, lastOut, where lastIn is the most recent time a system member fronted when they were not already switched in, and lastOut is the most recent time a system member stopped fronting
currentFronters - list of shortcodes of currently fronting system members

## Implimented functions

**rsSecondToFractal(rsSeconds)** takes in a period of time in seconds and converts it to a number of headspace fractals, designed to work with *datetime.total_seconds()*, returns an int

**hsFractalTohsTimeObject(hsFractals)** converts an int of headspace fractals into a headspace date time object, returns [cycles, seasons, weeks, days, segments, fractals]

**hsTimeNow()** gets the current time in headspace based on zeropoint in apikeys.json, returns [cycles, seasons, weeks, days, segments, fractals]

hsTimeShort(hsTimeObject)

hsTimeHuman(hsTimeObject)

rsLastSeen(member)

hsLastSeen(member)

## Missing functions

rsCurrentFrontingTime() - says how long each currently fronting person has been fronting for; returns list of objects with human readable member name, shortcode, realspace time interval elapsed since started fronting

pullPeriodic() - gets info about the most recent switch, and updates the list of current fronters and stats, and a boolean to indicate if the current fronter information has changed

INTERNAL:
updateMemberStats(stats, switches)
    given a batch of switches and existing member stats, updates the member stats with this information, and returns updated member stats

pullBackUp - fetches the system and member objects from the server, ideally run daily

### Maybe not implementable if using a microcontroller with a small amount of memory:

allTime(member) - if member is included returns their total fronting time, if no member provided returns a list of all members and each of their total fronting time

allPercent(member) - returns a list of all members and their percentage of fronting

recientTime(member) - returns the amount of time that a member has fronted for in the last cycle

recientPercent(member) - returns the percentage of time a member has been fronting for in the last cycle