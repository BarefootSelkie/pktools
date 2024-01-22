# pluralkit-time
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
