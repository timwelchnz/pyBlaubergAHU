import time
import math
from blaubergahu import AHU

ahu=AHU("<broadcast>", "1111" , "DEFAULT_DEVICEID" )

ips = ahu.search_devices('0.0.0.0')
print ( ips ) 

for addr in ips:
    print ( addr ) 
    ahu=AHU(addr, "1111" , "DEFAULT_DEVICEID" )
    ahu.init_device()
    ahu.update()
    
    # Print out all readable parameters
for i in ( ahu.params ):
    if ahu.params[i][0] in ['filter_timer_reset', 'reset_alarms']:
        continue
    attr = str(getattr(ahu , ahu.params[i][0]))
    print ( ahu.params[i][0] + ": " + attr)



#print (ips[0])
# ahu=AHU(ips[0], "1111" , "DEFAULT_DEVICEID" )
#ahu=AHU("10.94.0.108", "1111" , "DEFAULT_DEVICEID" )


# ahu.get_param( 'device_search' );
# print ( 'ahu_id: ' , ahu.device_search ) ;
# ahu.id=ahu.device_search ;

# ahu.set_man_speed(14);
# ahu.update();
# print ( 'man_speed: ' + ahu.man_speed )
# man_speed = 5
# ahu.set_param('man_speed', hex(math.ceil( man_speed * 255 / 100 )).replace("0x","").zfill(2) ) # hex(math.ceil( speed_in_% * 255 / 100 )).replace("0x","").zfill(2)
# print ( 'man_speed: ' + ahu.man_speed )

# ahu.set_param('state','toggle')

# ahu.set_param('state','off') #'on','off','toggle'
# ahu.set_param('speed','2') #'1','2','3','manual'
# print ( 'speed: ' + ahu.speed )


# print ( 'man_speed: ' + ahu.man_speed )
# print ( 'fan1_speed: ' + ahu.fan1_speed )
# print ( 'fan2_speed: ' + ahu.fan2_speed )
# print ( 'airflow: ' + ahu.airflow )

# Set examples
# ahu.set_param('state','toggle') #'on','off','toggle'
# print ( 'state: ' + ahu.state )
# ahu.set_param('speed','manual') #'low','medium','high','manual'
# print ( 'speed: ' + ahu.speed )

#man_speed = 4
# ahu.set_param('man_speed', hex(math.ceil( man_speed * 255 / 100 )).replace("0x","").zfill(2) ) # hex(math.ceil( speed_in_% * 255 / 100 )).replace("0x","").zfill(2)
# print ( 'man_speed: ' + ahu.man_speed )

# ahu.set_param('timer_mode','off') # 'off', 'night', 'party'
# print ( 'timer_mode: ' + ahu.timer_mode )
# ahu.update()
# print ( 'timer_counter: ' + ahu.timer_counter )

# ahu.set_param('humidity_sensor_state','on') # 'off', 'on', 'toggle'
# print ( 'humidity_sensor_state: ' + ahu.humidity_sensor_state )

# ahu.set_param('relay_sensor_state','off') # 'off', 'on', 'toggle'
# print ( 'relay_sensor_state: ' + ahu.relay_sensor_state )

# ahu.set_param('analogV_sensor_state','off') # 'off', 'on', 'toggle'
# print ( 'analogV_sensor_state: ' + ahu.analogV_sensor_state )

# ahu.set_param('humidity_treshold',hex(60).replace("0x","").zfill(2)) #hex(humidity_in_%).replace("0x","").zfill(2) 
# print ( 'humidity_treshold: ' + ahu.humidity_treshold )

# ahu.set_param('boost_time', hex(30).replace("0x","").zfill(2) ) # hex(minutes).replace("0x","").zfill(2)
# print ( 'boost_time: ' + ahu.boost_time )

#h=0
#m=38
#s=00
#ahu.set_param('rtc_time', hex(s).replace("0x","").zfill(2) + hex(m).replace("0x","").zfill(2) + hex(h).replace("0x","").zfill(2))
#print ( 'rtc_time: ' + ahu.rtc_time )

#day_in_week=5
#month=10
#day=8
#year=21
#ahu.set_param('rtc_date', hex(day).replace("0x","").zfill(2) + hex(day_in_week).replace("0x","").zfill(2) + hex(month).replace("0x","").zfill(2) + hex(year).replace("0x","").zfill(2))
#print ( 'rtc_date: ' + ahu.rtc_date )

#ahu.set_param('cloud_server_state','off') # 'off', 'on', 'toggle'
#print ( 'cloud_server_state: ' + ahu.cloud_server_state )

#ahu.set_param('airflow','heat_recovery') # 'ventilation', 'heat_recovery', 'air_supply'
#print ( 'airflow: ' + ahu.airflow )

#ahu.set_param('analogV_treshold',hex(50).replace("0x","").zfill(2)) #hex(analogV_treshold_%).replace("0x","").zfill(2) 
#print ( 'analogV_treshold: ' + ahu.analogV_treshold )

#h=8
#m=0
#ahu.set_param('night_mode_timer',hex(m).replace("0x","").zfill(2) + hex(h).replace("0x","").zfill(2)) 
#print ( 'night_mode_timer: ' + ahu.night_mode_timer )
#h=4
#m=0
#ahu.set_param('party_mode_timer', hex(m).replace("0x","").zfill(2) + hex(h).replace("0x","").zfill(2)) 
#print ( 'party_mode_timer: ' + ahu.party_mode_timer )

#ahu.do_func(ahu.func['read'] , "0077" )
#print ( 'weekly_schedule_setup: ' + ahu.weekly_schedule_setup ) 

#ahu.do_func(ahu.func['read'] , "0302" )
#print ( 'night_mode_timer: ' + ahu.night_mode_timer ) 

#ahu.do_func(ahu.func['read'] , "0305" )
#print ( 'analogV_status: ' + ahu.analogV_status ) 

#for i in range (1,8):
#    for j in range (1,5):
#        ahu.do_func(ahu.func['read'] , "0077" , hex(i).replace("0x","").zfill(2) + hex(j).replace("0x","").zfill(2)) # value select schedule Day/Period
#        print ( 'weekly_schedule_setup: ' + ahu.weekly_schedule_setup ) 
#        time.sleep(0.2)

# Write only parameters
# ahu.reset_filter_timer()
# ahu.reset_alarms()

#ahu.set_param('airflow','ventilation') # 'ventilation', 'heat_recovery', 'air_supply'
#print ( 'airflow: ' + ahu.airflow )

#ahu.set_param('airflow','air_supply') # 'ventilation', 'heat_recovery', 'air_supply'
#print ( 'airflow: ' + ahu.airflow )

#ahu.set_param('airflow','heat_recovery') # 'ventilation', 'heat_recovery', 'air_supply'
#print ( 'airflow: ' + ahu.airflow )


