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

## Missing functions

lastSeen(member) - returns when member was last seen based on member id

allTime(member) - if member is included returns their total fronting time, if no member provided returns a list of all members and each of their total fronting time

allPercent(member) - returns a list of all members and their percentage of fronting

recientTime(member) - returns the amount of time that a member has fronted for in the last cycle

recientPercent(member) - returns the percentage of time a member has been fronting for in the last cycle