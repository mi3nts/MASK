# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import datetime
import board
import busio
from i2cMints.i2c_bno080 import BNO080
from mintsXU4 import mintsSensorReader as mSR


from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C

from adafruit_extended_bus import ExtendedI2C as I2C

# i2c     = I2C(4)
# bno     = BNO08X_I2C(i2c)

debug        = False 
bus          = I2C(4)
bno080       = BNO080(bus,debug)
initTrials   = 5
loopInterval = 2
checkCurrent = 0 
checkTrials  = 0 
checkLimit   = 5


def main(loopInterval, checkTrials, checkCurrent ):
    bno080_valid   =  bno080.initiate(initTrials)
    startTime    = time.time()
    while True:
        try:
            print("======= BNO080 ========")
            if bno080_valid:
                bno080Data = bno080.read()
                
                if checkCurrent == bno080Data[-1]:
                    checkTrials = checkTrials + 1 
                else: 
                    checkTrials  = 0 
                    checkCurrent = bno080Data[-1]
                
                print(checkTrials)
                
                if checkTrials == 0:
                    print(bno080Data)
                    continue;

                if checkTrials > checkLimit :
                    print("Resetting BNO080")
                    bno080_valid   =  bno080.initiate(initTrials)
                    time.sleep(10)
                    continue;

                    #  mSR.BNO080WriteI2c(bno080Data)
    



            print("=======================")  
            startTime = mSR.delayMints(time.time() - startTime,loopInterval)

        except Exception as e:
            print(e)
            print("Resetting BNO080")
            bno080_valid   =  bno080.initiate(initTrials)
            time.sleep(10)
        
if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring Climate data for MASK")
    main(loopInterval, checkTrials, checkCurrent )

