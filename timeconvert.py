#!/usr/bin/env python3

import time
import datetime
import json
import os
import math

# lenghts of time units in headspace seconds
minutelength = 60 # 60 headspace seconds
segmentlength = minutelength * 60
daylength = segmentlength * 6
weeklength = daylength * 6
seasonlength = weeklength * 6
cyclelength = seasonlength * 6

def realspaceToHeadspace(rsSec):
    return math.floor(rsSec * (1.5))

def humanReadableHeadspaceTime(hsSec):
    remainder = hsSec
    cycles = hsSec // cyclelength
    remainder = hsSec % cyclelength
    seasons = remainder // seasonlength
    remainder = hsSec % seasonlength
    weeks = remainder // weeklength
    remainder = hsSec % weeklength
    days = remainder // daylength
    remainder = hsSec % daylength
    segments = remainder // segmentlength
    remainder = hsSec % segmentlength
    minutes = remainder // minutelength
    remainder = hsSec % minutelength

    return (f"{cycles:d} cycles, {seasons:d} seasons, {weeks:d} weeks, {days:d} days, {segments:d} segments, {minutes:d} minutes")
