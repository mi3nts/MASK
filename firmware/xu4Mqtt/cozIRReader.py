
#
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import sys

dataFolderReference    = mD.dataFolderReference
portIn                 = "/dev/ttyS0"

# For the time the sensor is on the chamber - There should be a separate code to calibrate the sensors
# This code is intended only for  continous reading of all sensor parametors 
# Helpful links 
#   https://cdn.shopify.com/s/files/1/0019/5952/files/AN007_Auto-Zero_Setting_CO2_Sensor_Revision_1.0_01_June_2020.pdf
#   https://cdn.shopify.com/s/files/1/0019/5952/files/CO2_Sensor_Evaluation_Kit_User_Guide_9_June_2021_Rev_1.4.pdf?v=1640009264
# https://cdn.shopify.com/s/files/1/0019/5952/files/CO2Meter-GSS-Cozir-A-User-Guide-Rev_4.1.pdf
# I can basically use a couple of functions
# One time point calibration ZERO IN FRESH AIR
    # Sets value of CO2 in ppm for zero-point setting in fresh air. Input value is scaled by CO2 value multiplier, see ‘.’ command.
    # P 10 7\r\n
    # P 11 208\r\n
# Long term calibration AUTO-ZERO FUNCTION
    # Sets the value of CO2 in ppm used for auto-zeroing. Input value is scaled by CO2 value multiplier, see ‘.’ command.
    # P 8 0\r\n
    # P 9 40\r\n
    # @ COMMAND (0x2E)
    # To disable auto-zeroing, send @ 0\r\n.
    # To start an auto-zeroing immediately, send 65222\r\n.
    # To determine the auto-zeroing configuration, send @\r\n. 

# On the live code 
#  Do the ALTITUDE COMPENSATION

# M #####\r\n Sets the number of measurement data  types output by the sensor. #####
# is the mask value   - Use 4096 + 64 + 4 + 2 = 4166 

# IF we have a proper CO2 Sensor 
# Fine Tune the zero point using F command - Comparison 
# Fine Tune the zero point using X command - Do it live 

# Have the serial numbe as well Y\r\n

baudRate = 9600

def main(portNum):

    menuSetUp = False

    ser = serial.Serial(
    port= portIn,\
    baudrate=baudRate,\
	parity  =serial.PARITY_NONE,\
	stopbits=serial.STOPBITS_ONE,\
	bytesize=serial.EIGHTBITS,\
    timeout=0)

    print(" ")
    print("Connected to: " + ser.portstr)
    print(" ")
    line = []

    ser.write(str.encode('K 2\r\n'))
    time.sleep(1)

    ser.write(str.encode('.\r\n'))
    time.sleep(1)

    ser.write(str.encode('z\r\n'))
    time.sleep(1)

    ser.write(str.encode('Z\r\n'))
    time.sleep(1)
    ser.write(str.encode('M 04166\r\n'))
    time.sleep(1)

    while True:
        try:
            for c in ser.read():
    
                line.append(chr(c))
                
                if chr(c) == '\n':
                     dataString = ''.join(line)
                     dataStringPost     = (''.join(line)).replace("\n","").replace("\r","")
                     print("================")
                     print(datetime.datetime.now())
                     print(dataStringPost)
                     time.sleep(5)
                     ser.write(str.encode('Q\r\n'))
                     line = []
        except:
            print("Incomplete read. Something may be wrong with {0}".format(portIn))
            line = []




if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring COZIR Sensor on port: {0}".format(portIn)+ " with baudrate " + str(baudRate))
    main(portIn)