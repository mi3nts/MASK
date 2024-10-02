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
loopInterval = 5
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
    preCheck = [-10.0,-10.0,-10.0]
    while bno080_initialized:
        try:
            startTime = mSR.delayMints(time.time() - startTime, loopInterval)
            bno080Data = bno080.readV2()
            print(bno080Data)
            if preCheck !=[bno080Data[7],bno080Data[8],bno080Data[9]]:
                print("Checked")

                # mSR.BNO080WriteI2c(bno080Data)
                preCheck = [bno080Data[7],bno080Data[8],bno080Data[9]]
            else:
                print("Values Have not changed")
                bno080.softReset()
                time.sleep(10)

        except Exception as e:
            print(f"An exception occurred: {type(e).__name__} – {e}")
            time.sleep(10)
            
            
            # # Attempt to reinitialize the sensor
            # bno080_initialized = bno080.initiate()
            
            # if not bno080_initialized:
            #     print("Failed to reinitialize BNO080 sensor. Exiting.")
            #     quit()  # Consider using a proper exit or exception handling mechanism
            
            # time.sleep(10)  # Optional second sleep, depending on your needs






if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring gyro data for MASK")
    main(loopInterval)