# pyBlaubergAHU

*** DISCLAIMER ***
I'm not a Python Programmer! 

I've forked https://github.com/aglehmann/pyEcovent/ as some of it worked on my Blauberg Komfort EC S Air Handling Unit (AHU)

I poked and prodded it and added parameters from the included PDF so that it worked better with my unit.

Python3 library for a Blauberg Komfort Air Handling Unit

## Install
	pip3 install pyBlaubergAHU

## Example usage
	from pyBlaubergAHU import AHU
	""" Create a new ahu with IP Address """
	""" The Ahu object takes 'host', 'name', 'port' as arguments """
	""" 'host' (IP address) is the only mandatory argument """
	""" 'name' is optional and will default to Home """
	""" 'port' is also optional and will default to 4000 """"
	ahu=AHU("192.168.0.22")
	
	""" Optinally create a AHU with a name  
	ahu=AHU("192.168.0.22", "Cellar AHU")

	""" Update the current values of the AHU """
	ahu.update()


	""" Print the current configured values """
	print(ahu.state)
	print(ahu.speed)
	print(ahu.man_speed)
	print(ahu.airflow)
	print(ahu.humidity)

	""" Set speed to medium (low=1 / medium=2 / high=3) """
	ahu.set_speed(2)
	print(ahu.speed)

	""" Set AHU state to off/on """
	ahu.set_state_off()
	ahu.set_state_on()

	""" Set manual speed to 123 (valid values 22 -> 255) """
	ahu.set_man_speed(123)
	print(ahu.man_speed)

	""" Set airflow to 'Air Supply' (ventilation=0 / heat recovery=1 / air supply=2)"""
	ahu.set_airflow(2)
	print(ahu.airflow)

## Intended usage
The intended usage of this library is to include Blauberg Komfort AHU's in <https://www.home-assistant.io/>

## Tested fans 
This library has only been tested on the following fans:
- [Blauberg Komfort EC S AHU](https://blaubergventilatoren.de/en/series/komfort-ec-sb-e)

