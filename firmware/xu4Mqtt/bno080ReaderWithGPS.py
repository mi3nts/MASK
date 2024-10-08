# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import datetime
import board
import busio
from i2cMints.i2c_bno080 import BNO080
from mintsXU4 import mintsSensorReader as mSR
import os
import sys
import subprocess
import adafruit_gps
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_extended_bus import ExtendedI2C as I2C

# i2c     = I2C(4)
# bno     = BNO08X_I2C(i2c)

debug        = False 
bus          = I2C(4)

time.sleep(1)
bno080       = BNO080(bus,debug)
initTrials   = 5
loopInterval = 1
checkCurrent = 0 
checkTrials  = 0 
checkLimit   = 5
changeTimes  = 0

def restart_program():
    """Restarts the current program."""
    print("Restarting program...")
    time.sleep(60.1)
    os.execv(sys.executable, ['python3'] + sys.argv)



def main(loopInterval):
    delta = 0
    resetDelta = 300
    lastGPRMC = time.time()
    lastGPGGA = time.time()



    for i in range(11):
        print(i)
        if(bno080.initiate()):
            print("bno080 Initialized")
            break
        time.sleep(30)
        if i == 10:
            print("bno080 not found")
            quit()
            
    gps = adafruit_gps.GPS_GtopI2C(bus, debug=False) # Use I2C interface
    print("GPS found")

    # Turn on everything (not all of it is parsed!)
    print("Sending GPS Command")
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    time.sleep(1)
    print("Changing Update Frequency")
    gps.send_command(b"PMTK220,100")
    changeTimes = 0
    startTime = time.time()
    preCheck = [-1.0,-1.0,-1.0]
    while True:
        try:
            startTime = mSR.delayMints(time.time() - startTime, loopInterval)
            bno080Data = bno080.read()
            print(bno080Data)
            if preCheck !=[bno080Data[11],bno080Data[12],bno080Data[13]]:
                preCheck =  [bno080Data[11],bno080Data[12],bno080Data[13]]
                changeTimes = 0 
                # print(bno080Data)
                # mSR.BNO080WriteI2c(bno080Data)  
            else:
                print("Values have not changed: " + str(changeTimes))
                changeTimes = changeTimes +1 
                if changeTimes >= 2:
                    changeTimes = 0 
                    time.sleep(30)
                    for i in range(11):
                        print(i)
                        if(bno080.initiate()):
                            print("bno080 Initialized")
                            break
                        time.sleep(30)
                        if i == 10:
                            print("bno080 Halted and Quitting")
                            quit()
            
            dateTime = datetime.datetime.now()
            dataString = gps.nmea_sentence
            print(dateTime)
            print(dataString)

            if (dataString.startswith("$GPGGA") or dataString.startswith("$GNGGA")) and mSR.getDeltaTime(lastGPGGA, delta):
                mSR.GPSGPGGA2Write(dataString, dateTime)
                lastGPGGA = time.time()

            if (dataString.startswith("$GPRMC") or dataString.startswith("$GNRMC")) and mSR.getDeltaTime(lastGPRMC, delta):
                mSR.GPSGPRMC2Write(dataString, dateTime)
                lastGPRMC = time.time()

        except Exception as e:
            print(f"An exception occurred: {type(e).__name__} – {e}")
            time.sleep(30)
            




if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring gyro data for MASK")
    main(loopInterval)