#!/usr/bin/python2

import fcntl
import time
import unittest

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

#data = [str(23),str(254)]
data = [94,254]
crc =  calculate_checksum(data , 2)

print crc
