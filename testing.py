#!/usr/bin/env python3

import requests
import json
import logging
import pktools 
import datetime

print("Current time : " + pktools.hsTimeHuman(pktools.hsTimeNow()) + "\n")

for member in pktools.memberSeen:
    who = pktools.getMember(member)["name"]

    print(str(who) + ": " + str(pktools.rsLastSeen(member)) + " = " + pktools.hsTimeShort(pktools.hsLastSeen(member)))
    