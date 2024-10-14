# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import datetime
import board
import busio
from i2cMints.i2c_icm20948 import ICM20948
from i2cMints.i2c_pa1010d import PA1010D
from mintsXU4 import mintsSensorReader as mSR
import os
import sys
import subprocess
from adafruit_extended_bus import ExtendedI2C as I2C

# i2c     = I2C(4)
# bno     = BNO08X_I2C(i2c)

debug        = False 

bus          = I2C(4)

time.sleep(1)

initTrials   = 5
loopInterval = 1
checkCurrent = 0 
checkTrials  = 0 
checkLimit   = 5
changeTimes  = 0

time.sleep(1)

pa1010d       = PA1010D(bus,debug)
icm20948      = ICM20948(bus,debug)


def main(loopInterval):


    delta = 0

    lastGPRMC = time.time()
    lastGPGGA = time.time()

    pa1010d.initiate()
    time.sleep(1)
    icm20948.initiate()
    time.sleep(1)
    
    startTime = time.time()



    while True:
        try:
            startTime = mSR.delayMints(time.time() - startTime, loopInterval)

            print("--------------------------------------------------------")
            print("--------------------------------------------------------")
            [fixFound, dateTime,dataString]  = pa1010d.read()
            print(dateTime)
            print(dataString)
            print(icm20948.read())

            if not(fixFound):
                continue

            if (dataString.startswith("$GPGGA") or dataString.startswith("$GNGGA")) and mSR.getDeltaTime(lastGPGGA, delta):
                mSR.GPSGPGGA2Write(dataString, dateTime)
                lastGPGGA = time.time()

            if (dataString.startswith("$GPRMC") or dataString.startswith("$GNRMC")) and mSR.getDeltaTime(lastGPRMC, delta):
                mSR.GPSGPRMC2Write(dataString, dateTime)
                lastGPRMC = time.time()


        except Exception as e:
            print(f"An exception occurred: {type(e).__name__} – {e}")
            time.sleep(1)
            


        
if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring gyro data for MASK")
    main(loopInterval)