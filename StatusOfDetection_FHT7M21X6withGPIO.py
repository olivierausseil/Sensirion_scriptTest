#!/usr/bin/python2
# ----------------- Initialization --------------------
#library import
import time
import logging
import sys

import argparse
import curses

from smbus2 import SMBus
import RPi.GPIO as GPIO

timeDetection = 0
endTimeDetection = 0
detection = 0
flagTime = 0
loopInfinite = True
choice = 0
finalTime = 0


ModeControlPin = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(ModeControlPin, GPIO.OUT)

# --- GPIO Initialization
def setNetworkMode() :
    GPIO.output(ModeControlPin,GPIO.HIGH)
    return

def setStandAloneMode() :
    GPIO.output(ModeControlPin,GPIO.LOW)
    return

def initControlModeGPIO():
    #ModeControlPin = 4
    setNetworkMode()
    return

#FORMAT = '%(asctime)s %(message)s',datefmt='%a %d %b %Y %H:%M:%S'
logging.basicConfig(level = logging.INFO,
                    format= '%(asctime)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')

bus = SMBus(1)
initControlModeGPIO()

#test on a bit who is interesting -> Method
def testBit(int_type, offset):
   mask = 1 << offset
   return(int_type & mask)

# -------------- End of initialization ----------------

while choice != ord('5'):
    screen = curses.initscr()

    screen.clear()
    screen.border(1)
    screen.addstr(2, 2, "Please choose the mode of operation (enter a number)...")
    screen.addstr(4, 4, "Stand-Alone    --> 1 ")
    screen.addstr(5, 4, "Network        --> 2")
    screen.addstr(6, 4, "GPIO HIGH      --> 3")
    screen.addstr(7, 4, "GPIO LOW       --> 4")
    screen.addstr(9, 4, "Exit           --> 5")
    screen.refresh()

    choice = screen.getch()

    loopInfinite = True # We give the possibility to come back on Network Mode

    if choice == ord('3'):
        GPIO.output(ModeControlPin,1)


    if choice == ord('4'):
        GPIO.output(ModeControlPin,0)

    if choice == ord('1'):
        curses.endwin()
        setStandAloneMode()
        print "Stand-Alone mode "
        time.sleep(1)

    # /////////////////////////// NETWORK MODE /////////////////////////////////
    if choice == ord('2'):
        curses.endwin()
        setNetworkMode()
        #loopInfinite = True # We give the possibility to come back on Network Mode

        # -----  parser -----
        parser = argparse.ArgumentParser()
        parser.add_argument('-sT', action='store', dest='sensitivityTrigger')
        parser.add_argument('-sG', action='store', dest='sensitivityGain')

        results = parser.parse_args()

        #------- Sensitivity --------
        # in case argument has not been provided
        if None == results.sensitivityGain:
            sensitivityGain = int(16)
        else:
            sensitivityGain = int(results.sensitivityGain)

        # manage argument limits (0-31)
        if sensitivityGain < 0:
            sensitivityGain = 0

        if sensitivityGain > 31:
            sensitivityGain = 31

        # from there, sensitivity takes a value between 0 and 31 in all cases
        print ("sensitivity Gain is: " + str(sensitivityGain) )



        if None == results.sensitivityTrigger:
            sensitivityTrigger = int(0)
        else:
            sensitivityTrigger = int(results.sensitivityTrigger)

        # manage argument limits (0-7)
        if sensitivityTrigger < 0:
            sensitivityTrigger = 0

        if sensitivityTrigger > 7:
            sensitivityTrigger = 7


        # from there, sensitivity takes a value between 0 and 7 in all cases
        print ("sensitivity Trigger is: " + str(sensitivityTrigger) )

        # sum of the two sensitivity
        sensitivity = (sensitivityTrigger << 5) +  sensitivityGain

        if sensitivityTrigger == 0 :
            sensitivity = sensitivityGain
        if sensitivityGain == 0 :
            sensitivity = sensitivityTrigger
        #print sensitivity
        #-------------- end sensitivity ---------

        # -------------- end parser  --------------

        # change of trigger parameter
        #data = [0,triggerTime]
        #bus.write_i2c_block_data(0x4c, 3, data)

        # Change the trigger value of  sensor detection
        #valueOfDetectionTime = input("Enter a value in second : ")
        #valueOfDetectionTime = valueOfDetectionTime * 10
        #data = [0,valueOfDetectionTime]
        #bus.write_i2c_block_data(0x4c, 3, data)

        time.sleep(0.1)

        # change of trigger parameter for the first time
        data = bus.read_i2c_block_data(0x4c, 1, 2)
        data[0] = 123
        data[1] = sensitivity
        bus.write_i2c_block_data(0x4c, 1, data)
        print data
        # read the value of the sensor when switch on detection or not
        readValue = bus.read_i2c_block_data(0x4c,8,2)
        readValue = map(int, readValue)

        # testing the bit
        detection = testBit(readValue[1],0)
        print ''
        if detection == 0 :
            print "Initial state of the sensor : \"no in detection\" "
            endTimeDetection = time.time()
        else :
            print "Initial state of the sensor :  \"detection \"  "
            timeDetection = time.time()

        print " Now, we enter to the test loop to see if an other detection occur\n "
        #

        while loopInfinite :
            readValue = bus.read_i2c_block_data(0x4c,8,2)
            readValue = map(int, readValue)
            detectionTemporary = testBit(readValue[1],0)

            #change the value of trigger during the execution of the test (does not currently work )
            # if str.keys(change) :
            #    valueOfDetectionTime = input("Enter a value in second : ")
            #    valueOfDetectionTime = valueOfDetectionTime * 10
            #    data = [0,valueOfDetectionTime]
            #    bus.write_i2c_block_data(0x4c, 3, data)

            # if the state is "No detection"
            if detection == 0 :
                if detection != detectionTemporary :
                    # change of state
                    #print("The sensor detects presence")
                    timeDetection = time.time()
                    detection = detectionTemporary
                    logging.info(' : DETECTION !!!!!!')
                    print ''
                    #logging.info(' : The sensor detects a presence !')

            if detection != 0 :
                if detection != detectionTemporary :
                    #print("End of the presence detection")
                    endTimeDetection = time.time()

                    detection = detectionTemporary
                    logging.info(' : End of detection')
                    flagTime = 1

            time.sleep(0.1)
            # for calculate the detection time
            if flagTime == 1 :
                finalTime = endTimeDetection - timeDetection
                print ("detection time : "+ "%.2f" % finalTime)
                print ''
                flagTime = 0

            if finalTime > 8 :
                loopInfinite = False
                print ("Out of network mode")
                time.sleep(1)


curses.endwin() # quit the graphic interface
GPIO.cleanup() # the GPIO come back to origin



        # for fill a list of time
        #L = []
        #def add(i, s):
        #    try:
        #        L[i] = s
        #    except IndexError:
        #        L.extend([None]*(i-len(L)+1))
        #        L[i] = s

    # ---- First idea -----
    # Wait for detection
    #while detection == 0:
    #    readValue = bus.read_i2c_block_data(0x4c,8,2)
    #    readValue = map(int, readValue)
    #    detection = testBit(readValue[1],0)
        #print (readValue)
        #print (detection)
    #    time.sleep(0.1)
    #    if detection:
    #        timeDetection = time.time()
    #        print("detection")
    #        print(time)
    #        break

    #Wait fot the end-detection
    #while detection != 0 :
    #    readValue = bus.read_i2c_block_data(0x4c,8,2)
    #    readValue = map(int, readValue)
    #    detection = testBit(readValue[1],0)

        #print (readValue)
        #print (detection)
    #    time.sleep(0.1)
    #    if detection == 0:
    #        time = time.strftime("%H:%M:%S")
    #        endTimeDetection = time.time()
    #        print("end detection")
    #        print(time)
    #        break
    #

    #finalTime = endTimeDetection - timeDetection
    #print ("detection time : "+ "%.2f" % finalTime)
    # print ("%.2f" % tempsfinal)
