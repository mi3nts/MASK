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
loopInterval = 1 
checkCurrent = 0 
checkTrails  = 0 
checkLimit   = 2


def main(loopInterval):
    bno080_valid   =  bno080.initiate(initTrials)
    startTime    = time.time()
    while True:
        try:
            print("======= BNO080 ========")
            if bno080_valid:
                bno080Data = bno080.read()
                if bno080Data == checkCurrent:
                    checkTrails = checkTrails + 1 
                
                if checkTrails >= checkLimit :
                    print("Resetting BNO080")
                    bno080_valid   =  bno080.initiate(initTrials)
                    time.sleep(10)
                    break;
                else: 
                    checkTrails = 0 

                bno080_valid   = bno080.initiate(initTrials)
                checkCurrent   = bno080Data[-1]
                print(bno080Data)
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
    main(loopInterval)


# while True:
#     print(datetime.datetime.now())
#     try:
#         time.sleep(5)
#         print("Acceleration:")
#         accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
#         print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
#         print("")

#         print("Gyro:")
#         gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
#         print("X: %0.6f  Y: %0.6f Z: %0.6f rads/s" % (gyro_x, gyro_y, gyro_z))
#         print("")

#         print("Magnetometer:")
#         mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
#         print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (mag_x, mag_y, mag_z))
#         print("")

#         print("Rotation Vector Quaternion:")
#         quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
#         print(
#             "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f"
#             % (quat_i, quat_j, quat_k, quat_real)
#         )
#         print("")
#     except:
#         print("Error")