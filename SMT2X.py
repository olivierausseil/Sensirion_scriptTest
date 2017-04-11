#!/usr/bin/python2

# A bug seen when i want use smbus : do this procedure
# sudo apt-get install build-essential libi2c-dev i2c-tools python-dev libffi-dev
# sudo pip install cffi
# sudo pip install smbus-cffi

from smbus import SMBus
from time import sleep

# I2C address of SHT21 ( datasheet_Sensirion_Humidity_Sensors_SHT21_Datasheet_V4.pdf __page 7 __ paragraph 5.3  )
I2CAdress = 0x40

# command codes ( datasheet_Sensirion_Humidity_Sensors_SHT21_Datasheet_V4.pdf __page 8 __ Table 6 )
TEM                 = 0xE3
HUM                 = 0xE5
WRITE_USER_REGISTER = 0xE6
READ_USER_REGISTER  = 0xE7

# command codes special ( datasheet_Sensirion_Humidity_Sensors_SHT2x_Electronic_Identification_Code_V1.1 )
CMD_ID = 0xFA0F

#THe I2C bus use on raspberry PI3
bus = SMBus(1)

#reading the identification numbers
ID_number = bus.read_word_data(I2CAdress, CMD_ID)
print format(ID_number,'04x')
sleep(0.1)

# Set the resolution to better possible : 0x02 --> 14 bits for temperature and 12 bits for humidity (datasheet_Sensirion_Humidity_Sensors_SHT21_Datasheet_V4.pdf __page 9 __ Table 8)
#bus.write_byte_data(I2CAdress,WRITE_USER_REGISTER,0x02)
# Read the user register for see if the resolution is like the specification
#user_register = bus.read_byte_data(I2CAdress, READ_USER_REGISTER)
#print format(user_register,'02x')

# reading raw humidity registers
raw_humidity = bus.read_word_data(I2CAdress, HUM)
data_humidity = [
                    (raw_humidity & 0xFF),
                    ( (raw_humidity >> 8) & 0xFF ),
                    ( (raw_humidity >> 16) & 0xFF ),
                    ( (raw_humidity>>24) & 0xFF )
                ]
print data_humidity

# reading raw temperature registers
raw_temperature = bus.read_word_data(I2CAdress, TEM)
data_temperature = [
                    (raw_temperature & 0xFF),
                    ( (raw_temperature >> 8) & 0xFF ),
                    ( (raw_temperature >> 16) & 0xFF ),
                    ( (raw_temperature>>24) & 0xFF )
                    ]

print data_temperature

# compute actual temperature
#  recover temperature word from raw temperature registers ( datasheet_Sensirion_Humidity_Sensors_SHT21_Datasheet_V4.pdf __page 10 __ paragraph 6 )
temp = data_temperature[0] * 256 + ( data_temperature[1] & 0xFC )
#  apply conversion formula ( atasheet_Sensirion_Humidity_Sensors_SHT21_Datasheet_V4.pdf __page 10 __ paragraph 6.1)
cTemp = -46.85 + (175.72 * temp / 65535.0)

#compute actual humidity
#  recover humidity word from raw temperature registers ( datasheet_Sensirion_Humidity_Sensors_SHT21_Datasheet_V4.pdf __page 10 __ paragraph 6 )
humidity = data_humidity[0] * 256 + ( data_humidity[1] & 0xFC )
#  apply humidity formula (datasheet_Sensirion_Humidity_Sensors_SHT21_Datasheet_V4.pdf __page 10 __ paragraph 6.2 )
humidityPercent = -6 + (125 * humidity / 65535)

# Output data to screen
print "Temperature in Celsius is : %.2f C" %cTemp
print "Relative Humidity is : %.2f %%RH" %humidityPercent
