#!/usr/bin/env python3

import pktools 
import time

pktools.pullPeriodic()

print("Current time : " + pktools.hsTimeHuman(pktools.hsTimeNow()) + "\n")

sorted_tuples = sorted(pktools.memberSeen.items(), key=lambda item: item[1]["lastIn"])
sorted_dict = {k: v for k, v in sorted_tuples}

for member in sorted_dict:
    who = pktools.getMember(member)["name"]

    print(str(who) + ": " + str(pktools.rsLastSeen(member)) + " = " + pktools.hsTimeShort(pktools.hsLastSeen(member)))

print("\nCurrent front : ")
for id in pktools.lastSwitch["members"]:
    member = pktools.getMember(id)
    print(member["name"] + ": " + str(pktools.rsSinceLastIn(id)) + " = " + str(pktools.hsSinceLastIn(id)))
print("\nWatching for new fronters:")

""" while True:
    if pktools.pullPeriodic():
        for id in pktools.lastSwitch["members"]:
            member = pktools.getMember(id)
            print(member["name"] + ": " + str(pktools.rsSinceLastIn(id)) + " = " + str(pktools.hsSinceLastIn(id)))
    time.sleep(10) """