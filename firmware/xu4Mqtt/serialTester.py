#
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import sys

dataFolder  = mD.dataFolder
ipsPort     = "/dev/ttyS0"
baudRate    = 9600

def main():
    ser = serial.Serial(
    port= ipsPort,\
    baudrate=baudRate,\
    parity  =serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

    print(" ")
    print("Connected to: " + ser.portstr)
    print(" ")

        #this will store the line
    line = []

    while True:
        try:
            for c in ser.read():
#                print(chr(c))
                line.append(chr(c))
                if chr(c) == '\n':
                    dataString     = (''.join(line))
                    dataStringPost = dataString.replace('\n', '')
                    print("================")
                    print(dataStringPost)
                    line = []
                    break
        except Exception as e:
            print(e)
            break   
    ser.close()


if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring IPS7100 on port: {0}".format(ipsPort) + " with baudrate " + str(baudRate))
    main()    