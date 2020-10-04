#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import datetime
   
s = None
def setup():
    global s
    s = serial.Serial('/dev/ttyAMA0',baudrate=9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1.0)
    time.sleep(5)
    print(s)

def readdata():
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    saveFileName = '/home/pi/Desktop/co2data/co2.txt' # + datetime.datetime.now().strftime("%Y%m") + 'CO2data.txt'
    
    b = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    s.write(b)
    time.sleep(5)
    
    result = s.read(9)
    time.sleep(5)
    print(result)
    print(len(result))

    if len(result) >= 9:
        print(result[2])
        print(result[3])
      
        #checksum = (0xFF*1 - ((result[1]*1+result[2]*1+result[3]*1+result[4]*1+result[5]*1+result[6]*1+result[7]*1)% 256))+ 0x01*1
        #checksumok = 'FAIL'

        #if checksum == result[8]:
        #  checksumok = 'PASS'
        
        data = '{}, {}\n'.format(now, str(result[2]*256+result[3]) #you can add checksumok
      
    else:
        data = '{}, nodata\n'.format(now) #FAIL
      
    print(data)
    file_data = open(saveFileName , "a" )
    file_data.write(data)
    file_data.close()
   
if __name__ == '__main__':
    setup()
    while True:
        readdata()