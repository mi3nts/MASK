# # SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# #
# # SPDX-License-Identifier: Unlicense
# import time
# import sys
# import datetime
# import board
# import busio
# from i2cMints.i2c_bno080 import BNO080
# from mintsXU4 import mintsSensorReader as mSR

# from adafruit_bno08x import (
#     BNO_REPORT_ACCELEROMETER,
#     BNO_REPORT_GYROSCOPE,
#     BNO_REPORT_MAGNETOMETER,
#     BNO_REPORT_ROTATION_VECTOR,
# )
# from adafruit_bno08x.i2c import BNO08X_I2C

# from adafruit_extended_bus import ExtendedI2C as I2C

# # i2c     = I2C(4)
# # bno     = BNO08X_I2C(i2c)

# debug = False 
# bus = I2C(4)
# bno080 = BNO080(bus, debug)
# initTrials = 5
# loopInterval = 2
# checkCurrent = 0 
# checkTrials = 0 
# checkLimit = 5

# def main(loopInterval, checkTrials, checkCurrent):
#     bno080_valid = bno080.initiate(initTrials)
#     startTime = time.time()
#     while True:
#         try:
#             print("======= BNO080 ========")
#             if bno080_valid:
#                 bno080Data = bno080.read()
#                 # print(bno080Data)
#                 if checkCurrent == bno080Data[12]:
#                     checkTrials += 1
#                 else:
#                     checkTrials = 0
#                     checkCurrent = bno080Data[12]

#                 print(checkTrials)
#                 # print(bno080Data)

#                 if checkTrials == 0:
#                     print("Writing Data")
#                     # print(bno080Data)
#                     mSR.BNO080WriteI2c(bno080Data)
#                     startTime = mSR.delayMints(time.time() - startTime, loopInterval)
#                     continue

#                 if checkTrials > checkLimit:
#                     print("Resetting BNO080")
#                     bno080_valid = bno080.initiate(initTrials)
#                     time.sleep(10)
#                     continue

#             startTime = mSR.delayMints(time.time() - startTime, loopInterval)
#             print("=======================")

#         except OSError as e:
#             print("OSError:", e)
#             print("Restarting script due to I2C communication error.")
#             time.sleep(10)
#             exec(open(sys.argv[0]).read())
#         except Exception as e:
#             print("Unexpected error:", e)
#             print("Restarting script due to unexpected error.")
#             time.sleep(10)
#             exec(open(sys.argv[0]).read())

# if __name__ == "__main__":
#     print("=============")
#     print("    MINTS    ")
#     print("=============")
#     print("Monitoring Climate data for MASK")
#     main(loopInterval, checkTrials, checkCurrent)
# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)

from adafruit_extended_bus import ExtendedI2C as I2C
from adafruit_bno08x.i2c import BNO08X_I2C

i2c     = I2C(4)
bno     = BNO08X_I2C(i2c)

bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

while True:
    time.sleep(0.5)
    print("Acceleration:")
    accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
    print("")

    print("Gyro:")
    gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f rads/s" % (gyro_x, gyro_y, gyro_z))
    print("")

    print("Magnetometer:")
    mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (mag_x, mag_y, mag_z))
    print("")

    print("Rotation Vector Quaternion:")
    quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
    print(
        "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real)
    )
    print("")