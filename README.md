# pktools

A set of tools to deal with time conversion functions, some are used by my whois projects, but several of these are only really applicable to my headspace. As I have a base 6 time system and wanted to be able to display that information in the real world.

### Implemented functions

**rsSecondToFractal(rsSeconds)** takes in a period of time in seconds and converts it to a number of headspace fractals, designed to work with *datetime.total_seconds()*, returns an int

**hsFractalTohsTimeObject(hsFractals)** converts an int of headspace fractals into a headspace date time object, returns [cycles, seasons, weeks, days, segments, fractals]

**hsTimeNow()** gets the current time in headspace based on zeropoint in apikeys.json, returns [cycles, seasons, weeks, days, segments, fractals]

hsTimeShort(hsTimeObject)

hsTimeHuman(hsTimeObject)

rsLastSeen(member)

hsLastSeen(member)

rsSinceLastIn(member)

hsSinceLastIn(member)
