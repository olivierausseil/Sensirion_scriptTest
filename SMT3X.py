#!/usr/bin/python2

import time
from smbus2 import SMBus # import library smbus2 compatible to use I2C
bus = SMBus(1)

I2CAdress = 0x44

bus.write_i2c_block_data(0x44, 0x2C, [0x06])

#time.sleep(0.5)

data = bus.read_i2c_block_data(I2CAdress,0x00,6) # go read the firmware version

#m1 = format(measurements[0],'02x')
#m2 = format(measurements[1],'02x')
#m3 = format(measurements[2],'02x')
#m4 = format(measurements[3],'02x')

#print ("measurements : " + m1 +"."+ m2+"."+ m3+"."+ m4) # display the value

# Convert the data
temp = data[0] * 256 + data[1]
cTemp = -45 + (175 * temp / 65535.0)
fTemp = -49 + (315 * temp / 65535.0)
humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

# Output data to screen
print "Temperature in Celsius is : %.2f C" %cTemp
#print "Temperature in Fahrenheit is : %.2f F" %fTemp
print "Relative Humidity is : %.2f %%RH" %humidity
