import obd
obd.logger.setLevel(obd.logging.DEBUG)
connection = obd.OBD("/dev/ttyUSB0") # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

print(response.value) # returns unit-bearing values thanks to Pint
print(response.value.to("mph")) # user-friendly unit conversions
