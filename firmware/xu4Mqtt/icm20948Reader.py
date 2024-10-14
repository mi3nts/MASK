# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import datetime
import board
import busio
from i2cMints.i2c_bno080 import BNO080
from i2cMints.i2c_pa1010d import PA1010D
from mintsXU4 import mintsSensorReader as mSR
import os
import sys
import subprocess
import adafruit_gps
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_icm20x
# i2c     = I2C(4)
# bno     = BNO08X_I2C(i2c)

debug        = False 

bus          = I2C(4)

time.sleep(1)

# BNO 
bno080       = BNO080(bus,debug)
initTrials   = 5
loopInterval = 1
checkCurrent = 0 
checkTrials  = 0 
checkLimit   = 5
changeTimes  = 0

time.sleep(1)

pa1010d       = PA1010D(bus,debug)

icm = adafruit_icm20x.ICM20948(bus)


def main(loopInterval):


    delta = 0
    resetDelta = 300
    lastGPRMC = time.time()
    lastGPGGA = time.time()

    # Fix to check a few times  
    pa1010d.initiate()

    # changeTimes = 0
    startTime = time.time()
    # preCheck = [-1.0,-1.0,-1.0]


    while True:
        try:
            startTime = mSR.delayMints(time.time() - startTime, loopInterval)

            print("--------------------------------------------------------")
            print("--------------------------------------------------------")
            [fixFound, dateTime,dataString]  = pa1010d.read()
            print(dateTime)
            print(dataString)
            print("Temperature    :{:.2f} C".format(*icm.temperature))
            print("Acceleration  X:{:.2f}, Y: {:.2f}, Z: {:.2f} m/s^2".format(*icm.acceleration))
            print("Gyro          X:{:.2f}, Y: {:.2f}, Z: {:.2f} rads/s".format(*icm.gyro))
            print("Magnetometer  X:{:.2f}, Y: {:.2f}, Z: {:.2f} uT".format(*icm.magnetic))


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
            time.sleep(10)
            


        
if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring gyro data for MASK")
    main(loopInterval)