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
from adafruit_bno08x.i2c import BNO08X_I2C
import subprocess
from adafruit_extended_bus import ExtendedI2C as I2C

# i2c     = I2C(4)
# bno     = BNO08X_I2C(i2c)

debug        = False 
bus          = I2C(4)

time.sleep(1)
bno080       = BNO080(bus,debug)
initTrials   = 5
loopInterval = 2.5
checkCurrent = 0 
checkTrials  = 0 
checkLimit   = 5

def restart_program():
    """Restarts the current program."""
    print("Restarting program...")
    time.sleep(60.1)
    os.execv(sys.executable, ['python3'] + sys.argv)


def main(loopInterval):
    bno080_initialized = bno080.initiate()
    print(bno080_initialized)
    startTime = time.time()
    preCheck = -10.0
    while bno080_initialized:
        try:
            startTime = mSR.delayMints(time.time() - startTime, loopInterval)
            bno080Data = bno080.readV2()
            # print(bno080Data)
            if preCheck !=bno080Data[11]:
                preCheck = bno080Data[11]
                mSR.BNO080V2WriteI2c(bno080Data)

            else:
                print("Values Have not changed")
                # bno080.hardReset()
                time.sleep(30)
                for i in range(10):
                    print(i)
                    if(bno080.initiate()):
                        break
                    time.sleep(30)



        except Exception as e:
            print(f"An exception occurred: {type(e).__name__} – {e}")
            time.sleep(30)
            




if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring gyro data for MASK")
    main(loopInterval)