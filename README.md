# pyBlaubergAHU

*** DISCLAIMER ***
I'm not a Python Programmer! 

I've forked https://github.com/aglehmann/pyEcovent/ as some of it worked on my Blauberg Komfort EC S Air Handling Unit (AHU)

I poked and prodded it and added parameters from the included PDF so that it worked better with my unit.

Python3 library for a Blauberg Komfort Air Handling Unit

## Install
	pip3 install pyBlaubergAHU

## Example usage
	from ecovent import Fan
	""" Create a new fan with IP Address """
	""" The Fan object takes 'host', 'name', 'port' as arguments """
	""" 'host' (IP address) is the only mandatory argument """
	""" 'name' is optional and will default to ecofan """
	""" 'port' is also optional and will default to 4000 """"
	fan=Fan("192.168.0.22")
	
	""" Optinally create a Fan with a name  
	fan=Fan("192.168.0.22", "Cellar Fan")

	""" Update the current values of the fan """
	fan.update()


	""" Print the current configured values """
	print(fan.state)
	print(fan.speed)
	print(fan.man_speed)
	print(fan.airflow)
	print(fan.humidity)

	""" Set speed to medium (low=1 / medium=2 / high=3) """
	fan.set_speed(2)
	print(fan.speed)

	""" Set fan state to off/on """
	fan.set_state_off()
	fan.set_state_on()

	""" Set manual speed to 123 (valid values 22 -> 255) """
	fan.set_man_speed(123)
	print(fan.man_speed)

	""" Set airflow to 'Air Supply' (ventilation=0 / heat recovery=1 / air supply=2)"""
	fan.set_airflow(2)
	print(fan.airflow)

## Intended usage
The intended usage of this library is to include Blauberg Komfort AHU's in <https://www.home-assistant.io/>

## Tested fans 
This library has only been tested on the following fans:
- [Blauberg Komfort EC S AHU](https://blaubergventilatoren.de/en/series/komfort-ec-sb-e)

