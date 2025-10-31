# _update_and_get_devices - Status: 200
x = {"devices":[{"name":"Green Light","value":"1","type":"LED","pin":"33"},{"name":"Water Tank Sensor","value":"100","type":"ULTRASONIC","pin":"5,18"},{"name":"RED LIGHT","value":"0","type":"LED","pin":"32"},{"name":"blue LIGHT","value":"0","type":"LED","pin":"25"},{"name":"FAN","value":"0","type":"FAN","pin":"15"}]}
# Received 5 devices from server
from rich import print
print(x)