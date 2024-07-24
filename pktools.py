#!/usr/bin/env python3

import datetime
### Constants ###

# Time constants for headspace
hsFractal = 1 # done like this to allow for future adding for smaller units
hsSegmentLen = hsFractal * 6
hsDayLen = hsSegmentLen * 6
hsWeekLen = hsDayLen * 6
hsSeasonLen = hsWeekLen * 6
hsCycleLen = hsSeasonLen * 6

# Labels
nameSeasons = ["Prevernal", "Vernal", "Estival", "Serotinal", "Autumnal", "Hibernal"]
symbolSeasons = ["🌧️", "🌱", "☀️", "🌾", "🍂", "❄️"]

labelDominoH = [["🀹","🀺","🀻","🀼","🀽","🀾"],
["🁀","🁁","🁂","🁃","🁄","🁅"],
["🁇","🁈","🁉","🁊","🁋","🁌"],
["🁎","🁏","🁐","🁑","🁒","🁓"],
["🁕","🁖","🁗","🁘","🁙","🁚"],
["🁜","🁝","🁞","🁟","🁠","🁡"]]

labelDominoV = [["🁫","🁬","🁭","🁮","🁯","🁰"],
["🁲","🁳","🁴","🁵","🁶","🁷"],
["🁹","🁺","🁻","🁼","🁽","🁾"],
["🂀","🂁","🂂","🂃","🂄","🂅"],
["🂇","🂈","🂉","🂊","🂋","🂌"],
["🂎","🂏","🂐","🂑","🂒","🂓"]]

labelDice = ["⚀","⚁","⚂","⚃","⚄","⚅"]

labelNumTrans = ["➀","➁","➂","➃","➄","➅","➆","➇","➈"]
labelNumFill = ["➊","➋","➌","➍","➎","➏","➐","➑","➒"]


### Data access functions ###

# Return information about a particular system member, and if the member is set to private
def getMember(memberID, pkMembers):
    member = [i for i in pkMembers if i["id"] == memberID][0]
    private = member["privacy"]["visibility"] == "private"
    return member, private    

### Time Converstion Functions ###

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
def hsTimeNow(zeropoint):
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

# Convert a headspace time to a string
# Returns: time in an easy to read format
def hsTimeEasy(hsTimeObject):
    if hsTimeObject[4] <= 3:
        hsTimeBlock = labelNumTrans[hsTimeObject[4]]
    else:
        hsTimeBlock = labelNumFill[hsTimeObject[4]]

    return (f"{hsTimeBlock} - {labelDominoV[hsTimeObject[2]][hsTimeObject[3]]} {nameSeasons[hsTimeObject[1]]} ( {symbolSeasons[hsTimeObject[1]]} ) {hsTimeObject[0]:d}")

### Member last seen, total front time, and percent fronted ###

# Get realsapce time elapsed since a memnber last started fronting
# Returns: integer of realspace seconds since the member started fronting
def rsSinceLastIn(member, memberSeen):
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
def rsLastSeen(member, memberSeen):
    rsTimeAgo = (datetime.datetime.utcnow() - toPythonDateTime(memberSeen[member]["lastOut"]))
    return (rsTimeAgo)

# Get headspace time elapsed since a member last stopped fronting
# Returns: integer of headspace fractals since the member stopped fronting
def hsLastSeen(member, memberSeen):
    rsTimeAgo = rsLastSeen(member, memberSeen)
    hsTimeAgo = hsFractalTohsTimeObject(
            rsSecondToFractal(
                rsTimeAgo.total_seconds()
            )
        )
    return(hsTimeAgo)
