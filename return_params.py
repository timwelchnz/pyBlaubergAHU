import sys
from blaubergahu import AHU
# Replace IP with your known AHU IP Address, Password and Device ID from that in the mobile app
ahu = AHU("192.168.1.230","1111", "001B00544656500C" ) 
result = ahu.update()
if result == False:
    print("Update unsuccessful - check IP Addr, Password, Device ID")
    sys.exit(1)

for i in ( ahu.params ):
    if ahu.params[i][0] in ['filter_timer_reset', 'reset_alarms']:
        continue
    attr = ahu.params[i][0]
    value = str(getattr(ahu , attr))
    NoOfSpaces = 26 - len(attr)
    attr = attr + ":"
    string_length = len(attr) + NoOfSpaces
    string_revised = attr.ljust(string_length)
    print ( string_revised, value)

print('')
print('Exhaust Temp: ' + ahu.exhaust_air_temp)
print('Extract Temp: ' + ahu.extract_air_temp)
print('Intake Temp: ' + ahu.intake_air_temp)
print('Supply Temp: ' + ahu.supply_air_temp)
