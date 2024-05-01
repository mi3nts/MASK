
#
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import sys

dataFolderReference    = mD.dataFolderReference
portIn                 = "/dev/ttyS0"


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
    time.sleep(2)


    ser.write(str.encode('.\r\n'))
    time.sleep(2)


    

    while True:
        try:
            for c in ser.read():
                line.append(chr(c))
                
                if chr(c) == '\n' and not(menuSetUp):
                    dataString = ''.join(line)
                    dataStringPost     = (''.join(line)).replace("\n","").replace("\r","")
                    print("================")
                    print(dataStringPost)
                    line = []

                    ser.write(str.encode('z'))
                    time.sleep(2)
                    # print("Setting Frequency to 10 Seconds")
                    # ser.write(str.encode('a'))
                    # time.sleep(2)
                    # ser.write(str.encode('1'))
                    # time.sleep(2)

                    # print("Setting Ozone Units to ppb")
                    # ser.write(str.encode('u'))
                    # time.sleep(2)
                    # ser.write(str.encode('0'))
                    # time.sleep(2)

                    # print("Setting Temperature Units to C")
                    # ser.write(str.encode('c'))
                    # time.sleep(2)
                    # ser.write(str.encode('1'))
                    # time.sleep(2)

                    # print("Setting Pressure Units to mbar")
                    # ser.write(str.encode('o'))
                    # time.sleep(2)
                    # ser.write(str.encode('1'))
                    # time.sleep(2)

                    # print("Exiting Menu")
                    # ser.write(str.encode('x'))
                    # time.sleep(2)
                    # menuSetUp = True
                    line = []

                if chr(c) == '\n' and (menuSetUp):
                    dataString = ''.join(line)
                    dataString     = (''.join(line)).replace("\n","").replace("\r","")
                    print(dataString)
                    # dateTime = datetime.datetime.now()

					# The Output shouldnt have any letters
                    # if(not(any(c.isalpha() for c in dataString))):
                    #     mSR.TB108LWrite(dataString,dateTime)
                    # line = []
        except:
            print("Incomplete read. Something may be wrong with {0}".format(portIn))
            line = []




if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring COZIR Sensor on port: {0}".format(portIn)+ " with baudrate " + str(baudRate))
    main(portIn)