#! /usr/bin/python3

import json
from blaubergahu import AHU
# Replace IP with your known AHU IP Address, Password and Device ID from that in the mobile app
ahu = AHU("192.168.1.230","1111", "001B00544656500C" )
result = ahu.update()
allsettings = {}
for i in ( ahu.params ):
    if ahu.params[i][0] in ['filter_timer_reset', 'reset_alarms']:
        continue
    allsettings[ahu.params[i][0]] = getattr(ahu,ahu.params[i][0])
json_string = json.dumps(allsettings)

# it's the two \n 's that stop header errors!
print('Content-Type: application/json; charset=utf-8\n\n')
if result == False:
    print("ERROR: Update unsuccessful - check IP Addr, Password, Device ID")
print(json_string)