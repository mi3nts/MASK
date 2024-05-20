
#
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import re

import sys

#  Set auto calibration 
##  Set calibration interval
##  Set Averaging intervals
##  



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

    print("Setting the sensor into polling mode")
    ser.write(str.encode('K 2\r\n'))
    time.sleep(1)
    
    print("Reading the altitude compensation value")
    ser.write(str.encode('s\r\n'))
    time.sleep(1)

    # print("Reading CO2 Data Point")
    # ser.write(str.encode('Z\r\n'))
    # time.sleep(1)
    
    # print("Setting COZIR to emit all data")
    # ser.write(str.encode('M 04166\r\n'))
    # time.sleep(1)
    
    # print("Asking for Data")
    # ser.write(str.encode('Q\r\n'))
    # time.sleep(1)

    while True:
        try:
            for c in ser.read():
                line.append(chr(c))
                if chr(c) == '\n':
                    print("-------------------------------------------------------------")
                    # print(datetime.datetime.now())                     
                    dataStringPost     = (''.join(line)).replace("\n","").replace("\r","").replace(" ","")
                    print(dataStringPost)
                    time.sleep(1)
                    if check_format(dataStringPost):
                        print(decode_cozir_data(dataStringPost))
                        ser.write(str.encode('Q\r\n'))

                     
                    line = []
        except:
            print("Incomplete read. Something may be wrong with {0}".format(portIn))
            line = []

def check_format(s):
    """
    Check if the string has the format 'H ddddd T ddddd Z ddddd z ddddd'.
    
    :param s: The string to check.
    :return: True if the string matches the format, False otherwise.
    """
    pattern = r'^H\d{5}T\d{5}Z\d{5}z\d{5}$'
    match   = re.match(pattern, s)
    return bool(match)

def decode_cozir_data(data):
    """
    Decodes COZIR sensor data from a formatted string.
    :param data: The string containing the sensor data.
    :return: A dictionary with decoded values.
    """
    print(data)
    try:     
        dateTime  = datetime.datetime.now()
        humidity      = int(data[1:6]) / 10.0             # Assuming the humidity is given in tenths of percentage
        temperature   = (int(data[7:12]) - 1000) / 10.0   # Assuming the temperature is given in tenths of degrees Celsius
        co2Filtured   = int(data[13:18])                  # CO2 concentration in ppm
        co2Recent     = int(data[19:])                    # Another CO2 concentration in ppm or another parameter
        return [dateTime,co2Recent,co2Filtured,temperature,humidity]
    
    except (IndexError, ValueError) as e:
        print(f"Error decoding data: {e}")
        return None

if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring COZIR Sensor on port: {0}".format(portIn)+ " with baudrate " + str(baudRate))
    main(portIn)