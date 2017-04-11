#!/usr/bin/python2

import time
import argparse

# the CRC calculation give by https://github.com/jaques/sht21_python/blob/master/sht21.py
# modification about this source, we take of the ord because we aren't in ASCII
def calculate_checksum(data, number_of_bytes):
        """5.7 CRC Checksum using the polynomial given in the datasheet"""
        # CRC
        POLYNOMIAL = 0x131  # //P(x)=x^8+x^5+x^4+1 = 100110001
        crc = 0
        # calculates 8-Bit checksum with given polynomial
        for byteCtr in range(number_of_bytes):
            #crc ^= (ord(data[byteCtr]))
            crc ^= (data[byteCtr])
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ POLYNOMIAL
                else:
                    crc = (crc << 1)
        return crc

def check_crc_tab(tab):
    if calculate_checksum(tab,2) == tab[2]:
        return True
    else:
        return False

# creation of PARSER : do argument when i launch the script
parser = argparse.ArgumentParser()
parser.add_argument('-f', action='store', dest='frame')
results = parser.parse_args()

# we storing the parameters in frame_character
frame_character = results.frame
#print frame_character

# get the last 12 characters
frame_character = frame_character[-12:]
#print frame_character

# after recover the last 12 characters, we create a tab of 6 integers
frame_int = []
for index in range(6):
    substrhex = frame_character[2*index:2*index+2]
    frame_int.append(int(substrhex, 16))

#print frame_int
# we separate the frame to 2 tabs
humidity_tab = frame_int[0:3]
temperature_tab = frame_int[3:6]

#print humidity_tab
#print temperature_tab


if check_crc_tab(humidity_tab) == False:
    print ("wrong_crc for humidity: " + str(humidity_tab))
else:
    print ("crc OK for humidity")

if check_crc_tab(temperature_tab) == False:
    print ("wrong_crc for temperature: " + str(temperature_tab))
else:
    print ("crc OK for temperature")

#get the humidity message
#frame_character_humidity_str = frame_character[:6]
#print frame_character_humidity_str

#convert str data to int data
#frame_character_humidity_int = []
#for frame_character_humidity_str in frame_character_humidity_str:
#    number = ord(frame_character_humidity_str) - 55
#    frame_character_humidity_int.append(number)
#print frame_character_humidity_int


#print frame_character_humidity
#print type(frame_character_humidity)

#get the temperature message
#frame_character_temperature = frame_character[-6:]
#print frame_character_temperature
