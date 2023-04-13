""" Version  """
__version__ = "0.1.0"

"""Library to handle communication over Wifi with Blauberg Komfort AHU"""
import socket
import sys
import time
import math

class AHU(object):
    """Class to communicate with the Blauberg Komfort EC S Air Handling Unit or AHU"""
    
    HEADER = f'FDFD'

    func = {
        'read': "01",
        'write': "02",
        'write_return': "03",
        'inc': "04",
        'dec': "05",
        'resp': "06"
    }
    states = {
        0: 'off',
        1: 'on' ,
        2: 'toggle'
    }

    speeds = {
         0: 'standby', # This isn't in the documentation but I'll leave it here from the Ecovent library
         1: '1', 
         2: '2', 
         3: '3', 
         4: '4',
         5: '5',
         0xff: 'manual' # This isn't in the documentation but I'll leave it here from the Ecovent library
    }

    timer_statuses = {
        0: 'Off',
        1: 'On',
        2: 'Invert'
    }

    timer_modes = {
        0: 'Standby',
        1: 'Speed 1',
        2: 'Speed 2',
        3: 'Speed 3',
        4: 'Speed 4',
        5: 'Speed 5'
    }

    statuses = {
        0: 'off', 
        1: 'on',
        2: 'invert' # whatever this means?
    }

    temp_sensors = {
        0: 'Exhaust Duct',
        1: 'External Sensor',
        2: 'Supply Duct'
    }
    
    filter_statuses = {
        0: 'Clean', 
        1: '1', # This isn't in the documentation but I'll leave it here from the Ecovent library
        2: '2', # This isn't in the documentation but I'll leave it here from the Ecovent library
        3: 'Filter replacement timer has been activated' 
    }

    airflows = {
        0: 'ventilation',
        1: 'heat_recovery', 
        2: 'air_supply' 
    } 

    alarms = {
        0: 'None', 
        1: 'alarm', 
        2: 'warning' 
    }
    
    days_of_week = {
        0: 'all days',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday',
        8: 'Mon-Fri',
        9: 'Sat-Sun',
    }  

    filters = {
        0: 'filter replacement not required' , 
        1: 'replace filter' 
    }

    main_heater_types = {
        0: 'Turn Off',
        1: 'Electric'
    }

    unit_types = {
                    0x0100: 'Komfort EC S AHU', # New unit type returned for the AHU
                    0x0300: 'Vento Expert A50-1/A85-1/A100-1 W V.2',  #I'll leave these in here but they probably won't work
                    0x0400: 'Vento Expert Duo A30-1 W V.2', #I'll leave these in here but they probably won't work
                    0x0500: 'Vento Expert A30 W V.2' } #I'll leave these in here but they probably won't work

    wifi_operation_modes = {
        1: 'client' ,
        2: 'ap' 
    }

    wifi_enc_types =  {  
            48: 'Open', 
            50: 'wpa-psk' , 
            51: 'wpa2_psk',  
            52: 'wpa_wpa2_psk' 
    } 

    wifi_dhcps = {
        0: 'STATIC', 
        1: 'DHCP', 
        2: 'Invert' 
    }
    
    params = {
        0x0001: [ 'state', states ],
        0x0002: [ 'speed', speeds ],
        0x0003: [ 'max_speed_num', None],
        0x0004: [ 'param_0x0004', None],
        0x0005: [ 'param_0x0005', None],
        0x0006: [ 'boost_status', statuses ],
        0x0007: [ 'timer_status', timer_statuses ],  # Timer Status
        0x0008: [ 'timer_mode', timer_modes], # Timer Mode
        # 0x0009: [ 'timer_setpoint_min', None],
        # 0x000a: [ 'timer_setpoint_hrs', None],
        0x000b: [ 'timer_counter', None ],
        0x000d: [ 'room_temp_setpoint_timer', NotImplemented],  # Room temperature setpoint in timer mode
        0x000e: [ 'param_0x000e', None],
        0x000f: [ 'humidity_sensor_state', states ],
        0x0014: [ 'relay_sensor_state', states ],
        0x0015: [ 'param_0x0015', None],
        0x0016: [ 'param_0x0016', None], 
        0x0017: [ 'param_0x0017', None],
        0x0018: [ 'room_temp_setpoint', None], # Room temperature setpoint in normal mode
        0x0019: [ 'humidity_treshold', None ], 
        0x001a: [ 'param_0x001a', None],
        0x001b: [ 'param_0x001b', None],
        0x001c: [ 'param_0x001c', None],
        0x001d: [ 'temp_sensor_control', temp_sensors],  # Selecting a temperature sensor for controlling room temperature
        0x001e: [ 'current_temp', None ],   # Current temperature controlling the room temperature
        0x001f: [ 'intake_air_temp', None],
        0x0020: [ 'supply_air_temp', None],
        0x0021: [ 'extract_air_temp', None],
        0x0022: [ 'exhaust_air_temp', None], # Current exhaust air temperature at the unit outlet
        0x0023: [ 'param0x23', None],
        0x0024: [ 'battery_voltage', None ],
        0x0025: [ 'humidity', None ],
        0x0026: [ 'param_0x0026', None],
        0x0027: [ 'param_0x0027', None],
        0x0028: [ 'param_0x0028', None],
        0x0029: [ 'param_0x0029', None],
        0x002a: [ 'param_0x002a', None],
        0x002b: [ 'param_0x002b', None],
        0x002c: [ 'param_0x002c', None],
        0x002d: [ 'analogV', None ], # Doesn't appear to be implemented in an AHU
        0x002e: [ 'param_0x002e', None],
        0x002f: [ 'param_0x002f', None],
        0x0030: [ 'param_0x0030', None],
        0x0031: [ 'param_0x0031', None],
        0x0032: [ 'boost_switch_status', statuses ],  # Read Only - Current Boost switch status
        0x0033: [ 'fire_alarm_sensor', None],  # Read Only - Current fire alarm sensor status
        0x0034: [ 'param_0x0034', None],
        0x0035: [ 'param_0x0035', None],
        0x0036: [ 'minimum_fan_speed', None],  # 0...100 %
        0x0037: [ 'maximum_fan_speed', None],  # Documentation repeats Minimum but surely this is Maximum
        0x003A: [ 'supply_fan_speed_mode1', None],
        0x003B: [ 'exhaust_fan_speed_mode1', None],
        0x003C: [ 'supply_fan_speed_mode2', None],
        0x003D: [ 'exhaust_fan_speed_mode2', None],
        0x003E: [ 'supply_fan_speed_mode3', None],
        0x003F: [ 'exhaust_fan_speed_mode3', None],
        0x0040: [ 'supply_fan_speed_mode4', None],
        0x0041: [ 'exhaust_fan_speed_mode4', None],
        0x0042: [ 'supply_fan_speed_mode5', None],
        0x0043: [ 'exhaust_fan_speed_mode5', None],
        0x0044: [ 'man_speed', None ],
        0x0045: [ 'param_0x0045', None],
        0x0046: [ 'param_0x0046', None],
        0x0047: [ 'param_0x0047', None],
        0x0048: [ 'param_0x0048', None],
        0x0049: [ 'param_0x0049', None],
        0x004a: [ 'fan1_speed', None ],
        0x004b: [ 'fan2_speed', None ],
        0x004c: [ 'param_0x004c', None],
        0x004d: [ 'param_0x004d', None],
        0x004e: [ 'param_0x004e', None],
        0x004f: [ 'param_0x004f', None],
        0x0051: [ 'param_0x0051', None],
        0x0052: [ 'param_0x0052', None],
        0x0053: [ 'param_0x0053', None],
        0x0054: [ 'param_0x0054', None ],
        0x0055: [ 'param_0x0055', None],
        0x0056: [ 'param_0x0056', None],
        0x0057: [ 'param_0x0057', None],
        0x0058: [ 'param_0x0058', None],
        0x0059: [ 'param_0x0059', None],
        0x005a: [ 'param_0x005a', None ],
        0x005b: [ 'param_0x005b', None ],
        0x005c: [ 'param_0x005c', None],
        0x005d: [ 'param_0x005d', None],
        0x005e: [ 'param_0x005e', None],
        0x005f: [ 'param_0x005f', None],
        0x0060: [ 'main_heater_type', main_heater_types],
        0x0061: [ 'param_0x0061', None],
        0x0062: [ 'param_0x0062', None],
        0x0063: [ 'param_0x0063', None],
        0x0064: [ 'filter_timer_countdown', None ],
        0x0066: [ 'boost_time', None ],
        # 0x0067: [ 'param_0x0067', None], # Not returned in an AHU
        # 0x0068: [ 'param_0x0068', None], # Not returned in an AHU
        # 0x0069: [ 'param_0x0069', None], # Not returned in an AHU
        # 0x006a: [ 'param_0x006a', None],
        # 0x006b: [ 'param_0x006b', None],
        # 0x006c: [ 'param_0x006c', None],
        # 0x006d: [ 'param_0x006d', None],
        # 0x006e: [ 'param_0x006e', None],
        0x006f: [ 'rtc_time', None ],
        0x0070: [ 'rtc_date', None ],
        0x0071: [ 'param_0x0071', None],
        0x0072: [ 'weekly_schedule_state', states],
        0x0073: [ 'weekly_schedule_speed', None], # Weekly schedule speed
        0x0074: [ 'weekly_schedule_temp', None], # Weekly schedule temperature setup
        # 0x0075: [ 'param_0x0075', None], # Not returned in an AHU
        # 0x0076: [ 'param_0x0076', None], # Not returned in an AHU
        0x0077: [ 'weekly_schedule_setup', None ], # Schedule setup Byte
        0x0078: [ 'param_0x0078', None],
        0x0079: [ 'param_0x0079', None],
        0x007a: [ 'param_0x007a', None ],
        0x007b: [ 'param_0x007b', None ],
        0x007c: [ 'device_search', None ],
        0x007d: [ 'device_password', None ],
        0x007e: [ 'motor_hours', None ],
        # 0x007F: [ 'current_alarms', None], # Urg, this errors when there are no alarms...
        # 0x0080: [ 'param_0x0080', None ], # Not returned in an AHU
        0x0081: [ 'param_0x0081', None ], # Heater status
        0x0082: [ 'param_0x0082', None ], 
        0x0083: [ 'alarm_status', alarms ],
        0x0084: [ 'param_0x0084', None ],
        0x0085: [ 'cloud_server_state', states ],
        0x0086: [ 'firmware', None ],
        # 0x0087: [ 'param_0x0087', None ], # Not returned in an AHU
        0x0088: [ 'filter_replacement_status', filter_statuses ],
        0x0089: [ 'param_0x0089', None ],
        # 0x0090: [ 'param_0x0090', None ],
        0x0091: [ 'param_0x0091', None ],
        0x0092: [ 'param_0x0092', None ],
        0x0093: [ 'param_0x0093', None ],
        0x0094: [ 'wifi_operation_mode', None ], # Wi-Fi operation mode
        0x0095: [ 'wifi_ssid', None ], # Wi-Fi name in Client mode
        0x0096: [ 'wifi_password', None ],
        0x0099: [ 'wifi_encryption_type', None], # Wi-Fi data encryption type 
        0x009a: [ 'wifi_freq_chan', None ], # Wi-Fi frequency channel
        0x009b: [ 'wifi_dhcp', None ], # Wi-Fi module DHCP 
        0x009c: [ 'wifi_ip', None ], # IP address assigned to Wi-Fi module
        0x009d: [ 'wifi_subnet_mask', None ], # Wi-Fi module subnet mask
        0x009e: [ 'wifi_gateway', None ], # Wi-Fi module subnet mask
        0x00a3: [ 'curent_wifi_ip', None ], # Current Wi-Fi module IP address
        0x00B6: [ 'elect_heater_status', None],
        0x00b9: [ 'unit_type', unit_types ],
        0x00F0: [ 'recirculation_damper', None],
        0x0401: [ 'sound_generator', None]
    }

    write_only_params = {
        0x0065: [ 'filter_timer_reset', None ],		# WRITE ONLY
        0x0080: [ 'reset_alarms', None ],	# WRITE ONLY        
        0x0087: [ 'factory_reset', None ],
        0x00a0: [ 'wifi_apply_and_quit', None ],
        0x00a2: [ 'wifi_discard_and_quit', None ],
        0x0094: [ 'wifi_operation_mode', wifi_operation_modes  ],
        0x0095: [ 'wifi_name' , None ],
        0x0096: [ 'wifi_pasword', None ],
        0x0099: [ 'wifi_enc_type', wifi_enc_types ],
        0x009a: [ 'wifi_freq_chnnel', None ],
        0x009b: [ 'wifi_dhcp', wifi_dhcps  ],
        0x009c: [ 'wifi_assigned_ip', None ],
        0x009d: [ 'wifi_assigned_netmask', None ],
        0x009e: [ 'wifi_main_gateway', None ],        
    }

    _name = None
    _host= None
    _port = None
    _id = None
    _password = None
    _state = None
    _speed = None
    _max_speed_num = None
    _boost_status = None
    _timer_status = None
    _timer_mode = None
    _timer_setpoint_min = None
    _timer_counter = None
    _humidity_sensor_state = None
    _relay_sensor_state = None
    _analogV_sensor_state = None
    _room_temp_setpoint = None
    _humidity_treshold = None
    _current_temp = 0
    _intake_air_temp = 0
    _supply_air_temp = 0
    _extract_air_temp = 0
    _exhaust_air_temp = 0
    _battery_voltage = 0
    _humidity = None
    _analogV = None
    _boost_switch_status = None
    _supply_fan_speed_mode1 = None
    _exhaust_fan_speed_mode1 = None
    _supply_fan_speed_mode2 = None
    _exhaust_fan_speed_mode2 = None
    _supply_fan_speed_mode3 = None
    _exhaust_fan_speed_mode3 = None
    _supply_fan_speed_mode4 = None
    _exhaust_fan_speed_mode4 = None
    _supply_fan_speed_mode5 = None
    _exhaust_fan_speed_mode5 = None
    _man_speed = None
    _fan1_speed = None
    _fan2_speed = None
    _main_heater_type = None
    _filter_timer_countdown = None
    _boost_time = None
    _rtc_time = None
    _rtc_date = None
    _weekly_schedule_state = None
    _weekly_schedule_setup = None
    _device_search = None
    _device_password = None
    _motor_hours = None
    _current_alarms = None
    _alarm_status = None
    _cloud_server_state = None
    _firmware = None
    _filter_replacement_status = None
    _wifi_operation_mode = None
    _wifi_name = None
    _wifi_pasword = None
    _wifi_enc_type = None
    _wifi_freq_chnnel = None
    _wifi_dhcp = None
    _wifi_assigned_ip = None
    _wifi_assigned_netmask = None
    _wifi_main_gateway = None
    _wifi_ip = None
    _curent_wifi_ip = None
    _elect_heater_status = None
    _analogV_treshold = None
    _unit_type = None
    _recirculation_damper = None
    _sound_generator = None

#    def __init__(self, host, password="1111", ahu_id="DEFAULT_DEVICEID", name="Home", port=4000 ):

    def __init__(self, host, password="1111", ahu_id="001B00544656500C", name="Home", port=4000 ):
        self._name = name
        self._host = host
        self._port = port
        self._type = "02"
        self._id = ahu_id
        self._pwd_size = 0
        self._password = password
        
    def init_device (self):
        if self._id == "DEFAULT_DEVICEID":
            self.get_param( 'device_search' )
            self._id = self.device_search
        if not self._id:
            return False
        return self.update()

    def search_devices (self, addr = "0.0.0.0", port = 4000 ):
        payload="FDFD021044454641554c545f44455649434549440431313131017cf805"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((addr, port))
        sock.settimeout(0.1)
        ips = []
        i = 10
        while ( i > 1 ):
            i = i - 1
            self._device_search = self._id
            if self._host is None:
                self._host = '<broadcast>'
            if self._port is None:
                self._port = port
            sock.sendto( bytes.fromhex(payload), (self._host, self._port))
            data, addr = sock.recvfrom(1024)
            self.parse_response(data)
            if self._device_search != "DEFAULT_DEVICEID":
                ips.append(addr[0])
                ips=list(set(ips))
            # time.sleep(0.1)
        sock.close()
        return ips

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.settimeout(0.1)
        self._socket_connected = False
        while not self._socket_connected:
            try:
                self.socket.connect((self._host, self._port))
                return self.socket
            except OSError:
                self.socket.close()
                return None

    def str2hex(self,str_msg):
        return "".join("{:02x}".format(ord(c)) for c in str_msg)
        
    def hex2str(self,hex_msg):
        return "".join( chr(int("0x" + hex_msg[i:(i+2)],16)) for i in range(0,len(hex_msg),2))

    def hexstr2tuple(self,hex_msg):
        return [int(hex_msg[i:(i+2)], 16) for i in range(0,len(hex_msg), 2)]
        
    def chksum(self,hex_msg):
        checksum = hex(sum(self.hexstr2tuple(hex_msg))).replace("0x","").zfill(4)
        byte_array = bytearray.fromhex(checksum)
        chksum = hex(byte_array[1]).replace("0x","").zfill(2) + hex(byte_array[0]).replace("0x","").zfill(2)
        return f"{chksum}"

    def get_size(self,str):
        return hex(len(str)).replace("0x","").zfill(2)

    def get_header(self):
        id_size = self.get_size(self._id)
        pwd_size = self.get_size (self._password)
        id = self.str2hex(self._id)
        password = self.str2hex(self._password)
        str = f"{self._type}{id_size}{id}{pwd_size}{password}"
        return str

    def get_params_index(self, value):
        for i in ( self.params ):
            if self.params[i][0] == value:
                return i
                
    def get_params_values(self, idx, value ):
        index = self.get_params_index(idx)
        if index != None:
            if self.params[index][1] != None:
                for i in (self.params[index][1]):
                    if self.params[index][1][i] == value:
                        return [ index , i ]
            return [ index, None ]
        else:
            return [ None, None ]

    def send(self, data):
        try:
            self.socket = self.connect()
            payload = self.get_header() + data
            payload = self.HEADER + payload + self.chksum(payload)
            response = self.socket.sendall( bytes.fromhex(payload))
            return response
        except socket.timeout:
            # print ( "BlaubergAHU: Connection timeout send to device: " + self._host , file = sys.stderr )
            return None

    def receive(self):
        try:
            response = self.socket.recv(1024)
            self.socket.close()
            return response
        except socket.timeout:
            # print ( "BlaubergAHU: Connection timeout receive from device: " + self._host , file = sys.stderr )
            self.socket.close()
            return ( False )

    def do_func (self, func, param, value="" ):
        out = ""
        parameter = ""
        for i in range (0,len(param), 4):
            n_out = ""
            out = param[i:(i+4)] ;
            if out == "0077" and value =="" :
                value="0101"
            if value != "":
                val_bytes = int(len(value) / 2 ) ;
            else:
                val_bytes = 0
            if out[:2] != "00":
                n_out = "ff" + out[:2]
            if val_bytes > 1:
                n_out += "fe" + hex(val_bytes).replace("0x","").zfill(2) + out[2:4]
            else:
                n_out += out[2:4]
            parameter += n_out  + value
            if out == "0077":
                value = ""
        data = func + parameter
        response = False
        i = 0
        while not response:
            i = i + 1
            self.send(data)
            response = self.receive()
            if response:
                self.parse_response(response)
                return True
            if i >= 10:
                # print ("BlaubergAHU: Timeout device: " + self._host + " bail out after " + str(i) + " retries" , file = sys.stderr )
                return False
            # time.sleep(0.1)

    def update(self):
        request = "";
        for param in self.params:
            request += hex(param).replace("0x","").zfill(4)
        return self.do_func(self.func['read'], request)

    def set_param ( self, param, value ):
        valpar = self.get_params_values (param, value)
        if valpar[0] !=  None:
            if valpar[1] != None:
                self.do_func( self.func['write_return'], hex(valpar[0]).replace("0x","").zfill(4), hex(valpar[1]).replace("0x","").zfill(2) )
            else:
                self.do_func( self.func['write_return'], hex(valpar[0]).replace("0x","").zfill(4), value )
                
    def get_param ( self, param ):
        idx = self.get_params_index (param)
        if idx !=  None:
                self.do_func( self.func['read'], hex(idx).replace("0x","").zfill(4) )
            
    def set_state_on(self):
        request = "0001";
        value = "01" ;
        if self.state ==  'off':
            self.do_func( self.func['write_return'] , request, value )

    def set_state_off(self):
        request = "0001";
        value = "00" ;
        if self.state ==  'on':
            self.do_func(self.func['write_return'] , request, value )

    def set_speed(self, speed):
        if speed >= 1 and speed <= 3:
            request = "0002" 
            value = hex(speed).replace("0x","").zfill(2)
            self.do_func ( self.func['write_return'], request, value )

    def set_man_speed_percent(self, speed):
        if speed >= 2 and speed <= 100: 
            request = "0044"
            value = math.ceil(255 / 100 * speed)
            value = hex(value).replace("0x","").zfill(2)
            self.do_func ( self.func['write_return'], request, value )
            request = "0002"
            value = "ff"
            self.do_func ( self.func['write_return'], request, value )

    def set_man_speed(self, speed):
        if speed >= 14 and speed <= 255:
            request = "0044"
            value = speed
            value = hex(value).replace("0x","").zfill(2)
            self.do_func ( self.func['write_return'], request, value )
            request = "0002"
            value = "ff"
            self.do_func ( self.func['write_return'], request, value )

    def set_airflow(self, val):
        if val >= 0 and val <= 2:
            request = "00b7"
            value = hex(val).replace("0x","").zfill(2)
            self.do_func ( self.func['write_return'], request, value )

    def parse_response(self,data):
        pointer = 20 ; # discard header bytes 
        length = len(data) - 2 ;
        pwd_size = data[pointer] 
        pointer += 1
        password = data[pointer:pwd_size]
        pointer += pwd_size
        function = data[pointer]
        pointer += 1
        # from here parsing of parameters begin
        payload=data[pointer:length]
        response = bytearray()
        ext_function = 0
        value_counter = 1
        high_byte_value = 0
        parameter = 1 ;
        for p in payload:
            if parameter and p == 0xff:
                ext_function = 0xff
                # print ( "def ext:" + hex(0xff) )
            elif parameter and p == 0xfe:
                ext_function = 0xfe
                # print ( "def ext:" + hex(0xfe) )
            elif parameter and p == 0xfd:
                ext_function = 0xfd
                # print ( "dev ext:" + hex(0xfd) )
            else:
                if ext_function == 0xff:
                    high_byte_value = p
                    ext_function = 1
                elif ext_function == 0xfe:
                    value_counter = p
                    ext_function = 2
                elif ext_function == 0xfd:
                    None
                else:
                    if ( parameter == 1 ):
                        # print ("appending: " + hex(high_byte_value))
                        response.append(high_byte_value)
                        parameter = 0
                    else:
                        value_counter -= 1
                    response.append(p)

            if value_counter <= 0:
                parameter = 1
                value_counter = 1
                high_byte_value = 0
                setattr ( self, self.params[int(response[:2].hex(),16)][0], response[2:].hex())
                response = bytearray()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, ip):
        try:
            socket.inet_aton(ip)
            self._host = ip
        except socket.error:
            sys.exit()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id
        
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = pwd

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = self.states[int(val)]

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, input):
        val = int (input, 16 )
        self._speed = self.speeds[val]
    
    @property
    def max_speed_num(self):
        return self._max_speed_num
    
    @max_speed_num.setter
    def max_speed_num(self, input):
        val = int (input, 16)
        self._max_speed_num = str(val)

    @property
    def boost_status(self):
        return self._boost_status

    @boost_status.setter
    def boost_status(self, input):
        val = int (input, 16 )
        self._boost_status = self.statuses[val]

    @property
    def timer_status(self):
        return self._timer_status

    @timer_status.setter
    def timer_status(self, input):
        val = int (input, 16 )
        self._timer_status = self.timer_statuses[val]
        
    @property
    def timer_mode(self):
        return self._timer_mode

    @timer_mode.setter
    def timer_mode(self, input):
        val = int (input, 16 )
        self._timer_mode = self.timer_modes[val]

    @property
    def timer_setpoint_min(self):
        return self._timer_setpoint_min
    
    @timer_setpoint_min.setter
    def timer_setpoint_min(self, input):
        val = int (input, 16 )
        self._timer_setpoint_min = self.timer_setpoint_min[val]

    @property
    def timer_counter(self):
        return self._timer_counter

    @timer_counter.setter
    def timer_counter(self, input):
        val = int(input,16).to_bytes(3,'big')
        self._timer_counter = str ( val[2] ) + "h " +str ( val[1] ) + "m " + str ( val[0] ) + "s " 

    @property
    def humidity_sensor_state(self):
        return self._humidity_sensor_state

    @humidity_sensor_state.setter
    def humidity_sensor_state(self, input):
        val = int (input, 16 )
        self._humidity_sensor_state = self.states[val]

    @property
    def relay_sensor_state(self):
        return self._relay_sensor_state

    @relay_sensor_state.setter
    def relay_sensor_state(self, input):
        val = int (input, 16 )
        self._relay_sensor_state = self.states[val]

    @property
    def analogV_sensor_state(self):
        return self._analogV_sensor_state

    @analogV_sensor_state.setter
    def analogV_sensor_state(self, input):
        val = int (input, 16 )
        self._analogV_sensor_state = self.states[val]

    @property
    def room_temp_setpoint(self):
        return self._room_temp_setpoint
    
    @room_temp_setpoint.setter
    def room_temp_setpoint(self, input):
        val = int(input, 16)
        self._room_temp_setpoint = str( val )

    @property
    def humidity_treshold (self):
        return self._humidity_treshold

    @humidity_treshold.setter
    def humidity_treshold(self, input):
        val = int (input, 16 )
        self._humidity_treshold = str( val )
    
    @property
    def current_temp (self):
        return self._current_temp
    
    @current_temp.setter
    def current_temp(self, input):
        val = int.from_bytes(int(input,16).to_bytes(2,'big'), byteorder='little', signed=True) / 10
        self._current_temp = str( val ) + " °C"

    @property
    def intake_air_temp (self):
        return self._intake_air_temp
    
    @intake_air_temp.setter
    def intake_air_temp(self, input):
        val = int.from_bytes(int(input,16).to_bytes(2,'big'), byteorder='little', signed=True) / 10
        self._intake_air_temp = str( val ) + " °C"

    @property
    def supply_air_temp (self):
        return self._supply_air_temp
    
    @supply_air_temp.setter
    def supply_air_temp(self, input):
        val = int.from_bytes(int(input,16).to_bytes(2,'big'), byteorder='little', signed=True) / 10
        self._supply_air_temp = str( val ) + " °C"

    @property
    def extract_air_temp (self):
        return self._extract_air_temp
    
    @extract_air_temp.setter
    def extract_air_temp(self, input):
        val = int.from_bytes(int(input,16).to_bytes(2,'big'), byteorder='little', signed=True) / 10
        self._extract_air_temp = str( val ) + " °C"

    @property
    def exhaust_air_temp (self):
        return self._exhaust_air_temp
    
    @exhaust_air_temp.setter
    def exhaust_air_temp(self, input):
        val = int.from_bytes(int(input,16).to_bytes(2,'big'), byteorder='little', signed=True) / 10
        self._exhaust_air_temp = str( val ) + " °C"

    @property
    def battery_voltage (self):
        return self._battery_voltage

    @battery_voltage.setter
    def battery_voltage(self, input):
        val = int.from_bytes(int(input,16).to_bytes(2,'big'), byteorder='little', signed=False)
        self._battery_voltage = str( val ) + " mV"

    @property
    def humidity (self):
        return self._humidity

    @humidity.setter
    def humidity(self, input):
        val = int (input, 16 )
        self._humidity = str( val )

    @property
    def analogV (self):
        return self._analogV

    @analogV.setter
    def analogV(self, input):
        val = int (input, 16 )
        self._analogV = str( val )

    @property
    def boost_switch_status (self):
        return self._boost_switch_status

    @boost_switch_status.setter
    def boost_switch_status(self, input):
        val = int (input, 16 )
        self._boost_switch_status = self.statuses[val]

# Below here is all the fan speeds
# Supply Fan Mode 1

    @property
    def supply_fan_speed_mode1 (self):
        return self._supply_fan_speed_mode1
    
    @supply_fan_speed_mode1.setter
    def supply_fan_speed_mode1(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._supply_fan_speed_mode1 = int( val / 255 * 100)

# Exhaust Fan Mode 1 
    @property
    def exhaust_fan_speed_mode1 (self):
        return self._exhaust_fan_speed_mode1
    
    @exhaust_fan_speed_mode1.setter
    def exhaust_fan_speed_mode1(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._exhaust_fan_speed_mode1 = int( val / 255 * 100)

# Supply Fan Mode 2

    @property
    def supply_fan_speed_mode2 (self):
        return self._supply_fan_speed_mode2
    
    @supply_fan_speed_mode2.setter
    def supply_fan_speed_mode2(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._supply_fan_speed_mode2 = int( val / 255 * 100)

# Exhaust Fan Mode 2 
    @property
    def exhaust_fan_speed_mode2 (self):
        return self._exhaust_fan_speed_mode2
    
    @exhaust_fan_speed_mode2.setter
    def exhaust_fan_speed_mode2(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._exhaust_fan_speed_mode2 = int( val / 255 * 100)

# Supply Fan Mode 3

    @property
    def supply_fan_speed_mode3 (self):
        return self._supply_fan_speed_mode3
    
    @supply_fan_speed_mode3.setter
    def supply_fan_speed_mode3(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._supply_fan_speed_mode3 = int( val / 255 * 100)

# Exhaust Fan Mode 3 
    @property
    def exhaust_fan_speed_mode3 (self):
        return self._exhaust_fan_speed_mode3
    
    @exhaust_fan_speed_mode3.setter
    def exhaust_fan_speed_mode3(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._exhaust_fan_speed_mode3 = int( val / 255 * 100)

# Supply Fan Mode 4

    @property
    def supply_fan_speed_mode4 (self):
        return self._supply_fan_speed_mode4
    
    @supply_fan_speed_mode4.setter
    def supply_fan_speed_mode4(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._supply_fan_speed_mode4 = int( val / 255 * 100)

# Exhaust Fan Mode 4 
    @property
    def exhaust_fan_speed_mode4 (self):
        return self._exhaust_fan_speed_mode4
    
    @exhaust_fan_speed_mode4.setter
    def exhaust_fan_speed_mode4(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._exhaust_fan_speed_mode4 = int( val / 255 * 100)

# Supply Fan Mode 5

    @property
    def supply_fan_speed_mode5 (self):
        return self._supply_fan_speed_mode5
    
    @supply_fan_speed_mode5.setter
    def supply_fan_speed_mode5(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._supply_fan_speed_mode5 = int( val / 255 * 100)

# Exhaust Fan Mode 5 
    @property
    def exhaust_fan_speed_mode5 (self):
        return self._exhaust_fan_speed_mode5
    
    @exhaust_fan_speed_mode5.setter
    def exhaust_fan_speed_mode5(self, input):
        val = int(input, 16 )
        if val >= 0 and val <= 255:
            self._exhaust_fan_speed_mode5 = int( val / 255 * 100)

# Above here is all the fan speeds

    @property
    def man_speed(self):
        return self._man_speed

    @man_speed.setter
    def man_speed(self, input ):
        val =  int(input,16)
        if val >= 0 and val <= 255:
            self._man_speed = int( val / 255 * 100)
        
    @property
    def fan1_speed(self):
        return self._fan1_speed

    @fan1_speed.setter
    def fan1_speed(self, input ):
        val = int.from_bytes(int(input,16).to_bytes(2,'big'), byteorder='little', signed=False)
        self._fan1_speed = str ( val )
        
    @property
    def fan2_speed(self):
        return self._fan2_speed

    @fan2_speed.setter
    def fan2_speed(self, input ):
        val = int.from_bytes(int(input,16).to_bytes(2,'big'), byteorder='little', signed=False)
        self._fan2_speed = str ( val )

    @property
    def main_heater_type(self):
        return self._main_heater_type
    
    @main_heater_type.setter
    def main_heater_type(self, input):
        val = int (input, 16 )
        self._main_heater_type = str( val )

    @property
    def filter_timer_countdown(self):
        return self._filter_timer_countdown

    @filter_timer_countdown.setter
    def filter_timer_countdown(self, input ):
        val = int(input[:6],16).to_bytes(3,'big')
        self._filter_timer_countdown = str ( val[2] ) + "d " +str ( val[1] ) + "h " + str ( val[0] ) + "m " 

    @property
    def boost_time (self):
        return self._boost_time

    @boost_time.setter
    def boost_time(self, input):
        val = int (input, 16 )
        self._boost_time = str( val ) + " m"

    @property
    def rtc_time(self):
        return self._rtc_time

    @rtc_time.setter
    def rtc_time(self, input ):
        val = int(input,16).to_bytes(3,'big')
        
        self._rtc_time = str ( val[2] ) + "h " +str ( val[1] ) + "m " + str ( val[0] ) + "s " 

    @property
    def rtc_date(self):
        return self._rtc_date

    @rtc_date.setter
    def rtc_date(self, input ):
        val = int(input,16).to_bytes(4,'big')
        self._rtc_date = str ( val[1] ) + " 20" + str ( val[3] ) + "-" +str ( val[2] ).zfill(2 ) + "-" + str( val[0] ).zfill(2 )

    @property
    def weekly_schedule_state(self):
        return self._weekly_schedule_state

    @weekly_schedule_state.setter
    def weekly_schedule_state(self, val):
        self._weekly_schedule_state = self.states[int(val)]

    @property
    def weekly_schedule_setup(self):
        return self._weekly_schedule_setup

    @weekly_schedule_setup.setter
    def weekly_schedule_setup(self, input):
        val = int(input,16).to_bytes(6,'big')
        self._weekly_schedule_setup = self.days_of_week[val[0]] + '/' + str(val[1]) + ': to ' + str(val[5]) + 'h ' + str(val[4]) + 'm ' + self.speeds[val[2]]

    @property
    def device_search(self):
        return self._device_search

    @device_search.setter
    def device_search(self, val):
        self._device_search = self.hex2str(val)
        
    @property
    def device_password(self):
        return self._device_password

    @device_password.setter
    def device_password(self, val):
        self._device_password = self.hex2str(val)        

    @property
    def motor_hours(self):
        return self._motor_hours

    @motor_hours.setter
    def motor_hours(self, input ):
        val = int(input,16).to_bytes(4,'big')
        self._motor_hours = str ( int.from_bytes(val[2:3],'big') ) + "d " + str ( val[1] ) + "h " +str ( val[0] ) + "m "

    @property
    def current_alarms(self):
        return self._current_alarms
    
    @current_alarms.setter
    def current_alarms(self, input):
        val = int(input,16)
        if self._alarm_status != "none": # If there are no alarms then there is no current alarms to display!
            self._current_alarms = str (val)

    @property
    def alarm_status (self):
        return self._alarm_status

    @alarm_status.setter
    def alarm_status(self, input):
        val = int (input, 16 )
        self._alarm_status = self.alarms[val]

    @property
    def cloud_server_state (self):
        return self._cloud_server_state

    @cloud_server_state.setter
    def cloud_server_state(self, input):
        val = int (input, 16 )
        self._cloud_server_state = self.states[val]

    @property
    def firmware (self):
        return self._firmware

    @firmware.setter
    def firmware(self, input):
        val = int(input,16).to_bytes(6,'big')
        self._firmware = str(val[0]) + '.' + str(val[1]) + " " + str(int.from_bytes(val[4:6], byteorder='little', signed=False)) + "-" + str ( val[3] ).zfill(2) + "-" +str ( val[2] ).zfill(2)

    @property
    def filter_replacement_status (self):
        return self._filter_replacement_status

    @filter_replacement_status.setter
    def filter_replacement_status(self, input):
        val = int (input, 16 )
        self._filter_replacement_status = self.filter_statuses[val]

    @property
    def wifi_operation_mode (self):
        return self._wifi_operation_mode

    @wifi_operation_mode.setter
    def wifi_operation_mode(self, input):
        val = int (input, 16 ) 
        self._wifi_operation_mode = self.wifi_operation_modes[val]

    @property
    def wifi_name (self):
        return self._wifi_name

    @wifi_name.setter
    def wifi_name(self, input):
        self._wifi_name = self.hex2str(input)

    @property
    def wifi_pasword (self):
        return self._wifi_pasword

    @wifi_pasword.setter
    def wifi_pasword(self, input):
        self._wifi_pasword = self.hex2str(input)
        
    @property
    def wifi_enc_type (self):
        return self._wifi_enc_type

    @wifi_enc_type.setter
    def wifi_enc_type(self, input):
        val = int (input, 16 )
        self._wifi_enc_type = self.wifi_enc_types[val]        
        
    @property
    def wifi_freq_chnnel (self):
        return self._wifi_freq_chnnel

    @wifi_freq_chnnel.setter
    def wifi_freq_chnnel(self, input):
        val = int (input, 16 )
        self._wifi_freq_chnnel = str(val)                

    @property
    def wifi_dhcp (self):
        return self._wifi_dhcp

    @wifi_dhcp.setter
    def wifi_dhcp(self, input):
        val = int (input, 16 )
        self._wifi_dhcp = self.wifi_dhcps[val]

    @property
    def wifi_assigned_ip (self):
        return self._wifi_assigned_ip

    @wifi_assigned_ip.setter
    def wifi_assigned_ip(self, input):
        val = int(input,16).to_bytes(4,'big')
        self._wifi_assigned_ip = str(val[0]) + '.' + str(val[1]) + "." + str(val[2]) + "." + str ( val[3] )

    @property
    def wifi_assigned_netmask (self):
        return self._wifi_assigned_netmask

    @wifi_assigned_netmask.setter
    def wifi_assigned_netmask(self, input):
        val = int(input,16).to_bytes(4,'big')
        self._wifi_assigned_netmask = str(val[0]) + '.' + str(val[1]) + "." + str(val[2]) + "." + str ( val[3] )

    @property
    def wifi_main_gateway (self):
        return self._wifi_main_gateway

    @wifi_main_gateway.setter
    def wifi_main_gateway(self, input):
        val = int(input,16).to_bytes(4,'big')
        self._wifi_main_gateway = str(val[0]) + '.' + str(val[1]) + "." + str(val[2]) + "." + str ( val[3] )

    @property
    def wifi_ip (self):
        return self._wifi_ip

    @wifi_ip.setter
    def wifi_ip(self, input):
        val = int(input,16).to_bytes(4,'big')
        self._wifi_ip = str(val[0]) + '.' + str(val[1]) + "." + str(val[2]) + "." + str ( val[3] )

    @property
    def curent_wifi_ip (self):
        return self._curent_wifi_ip

    @curent_wifi_ip.setter
    def curent_wifi_ip(self, input):
        val = int(input,16).to_bytes(4,'big')
        self._curent_wifi_ip = str(val[0]) + '.' + str(val[1]) + "." + str(val[2]) + "." + str ( val[3] )

    @property
    def elect_heater_status (self):
            return self._elect_heater_status
    
    @elect_heater_status.setter
    def elect_heater_status(self, input):
        val = int(input, 16)
        self._elect_heater_status = str(val)

    @property
    def unit_type (self):
        return self._unit_type

    @unit_type.setter
    def unit_type(self, input):
        val = int (input, 16 )
        self._unit_type = self.unit_types[val] 

    @property
    def recirculation_damper (self):
        return self._recirculation_damper
    
    @recirculation_damper.setter
    def recirculation_damper(self, input):
        val = int (input, 16)
        self._recirculation_damper = str(val)

    @property
    def sound_generator (self):
        return self._sound_generator
    
    @sound_generator.setter
    def sound_generator(self, input):
        val = int (input, 16)
        self._sound_generator = str(val)

    def reset_filter_timer(self):
        self.set_param('filter_timer_reset', "")

    def reset_alarms (self):
        self.set_param('reset_alarms', "")
