# pktools
A set of useful tools that run on a rasberry pi to handle automatic switching out, displaying who's fronting, and tracking time since fronted. I use this to display this data on serval different iot devices with different information, and also to push information to my qcf discord. It is built as a server - client system to allow for one device to handle all the fetching of infomation from plural kit so as to not hit their servers so hard.

**WARNING: This will create a copy of your pluralkit system on your local network, make sure your firewall and sercurity settings are good enough that you are happy doing this**

## Data files

Data files are stored locally in **~/.pktools**

**memberSeen** dictionary from shortCode to lastIn, lastOut, where lastIn is the most recent time a system member fronted when they were not already switched in, and lastOut is the most recent time a system member stopped fronting

**lastSwitch** switch object from pluralkit describing the most recent known switch

**pkMembers** full list of system members and information about these members pulled from PluralKit [see PluralKit documentation](https://pluralkit.me/api/models/)

**pkSwitches** backup of all switches pulled from PluralKit ( cureent only pulled by initialise and used for backup - future use in other stats )

**pkSystem** data pulled from PluralKit about the system itself (e.g. system name) [see PluralKit documentation](https://pluralkit.me/api/models/)

## pktools.py
This is the main client side libary designed to be added to other projects by import, it handles getting data from the data store. 

It also includes some time conversion functions that are only really applicable to my headspace as I have a base 6 time system and wanted to be able to display that informaiton in the real world.

### Implimented functions

**rsSecondToFractal(rsSeconds)** takes in a period of time in seconds and converts it to a number of headspace fractals, designed to work with *datetime.total_seconds()*, returns an int

**hsFractalTohsTimeObject(hsFractals)** converts an int of headspace fractals into a headspace date time object, returns [cycles, seasons, weeks, days, segments, fractals]

**hsTimeNow()** gets the current time in headspace based on zeropoint in apikeys.json, returns [cycles, seasons, weeks, days, segments, fractals]

hsTimeShort(hsTimeObject)

hsTimeHuman(hsTimeObject)

rsLastSeen(member)

hsLastSeen(member)

rsSinceLastIn(member)

hsSinceLastIn(member)

## pktsreve.py

This is the bridge between local 

## swtichout.py
This is a very simple script that simply swtiches all fronters out when run, it is designed to be run by a cron job to swtich out when I've fallen asleep, so that people don't log time when I'm actually just asleep.

### Cron job for switchout.py

``0 0 * * * cd /home/pi && python3 ./switchout.py``

## Implimented functions

pullMemberSeen()

pullPeriodic() - gets info about the most recent switch, and updates the list of current fronters and stats, and a boolean to indicate if the current fronter information has changed


## Missing functions

pullSystem()
pullMembers()

### Maybe not implementable if using a microcontroller with a small amount of memory:

allTime(member) - if member is included returns their total fronting time, if no member provided returns a list of all members and each of their total fronting time

allPercent(member) - returns a list of all members and their percentage of fronting

recientTime(member) - returns the amount of time that a member has fronted for in the last cycle

recientPercent(member) - returns the percentage of time a member has been fronting for in the last cycle

## Old readme.md stuff

### initialise.py

this is a script to completely rebuild all the data stores from scratch, it will overwrite any existing data with a download from pluralkit. it's intended to be run the first time the library is installed, or if something has gone so wrong that you need to scrape all the data and start over. it builds the following files:

- pkSystem.json
- pkMembers.json
- pkGroups.json
- pkSwitches.json

it can also be used to backup pluralket systems

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
