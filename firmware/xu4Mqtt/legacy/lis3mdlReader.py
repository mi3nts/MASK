import time
import datetime
import board
import busio
from mintsXU4 import mintsSensorReader as mSR
import os
import sys

import subprocess

from adafruit_lsm6ds.lsm6ds3 import LSM6DS3 as LSM6DS
from adafruit_lis3mdl import LIS3MDL


from adafruit_extended_bus import ExtendedI2C as I2C


debug        = False 
bus          = I2C(4)


time.sleep(1)

accel_gyro = LSM6DS(bus)
mag 	   = LIS3MDL(bus)


while True:
    #try:
    acceleration = accel_gyro.acceleration
    gyro = accel_gyro.gyro
    magnetic = mag.magnetic
    
    print(
        "Acceleration: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} m/s^2".format(*acceleration)
        )
    print("Gyro          X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} rad/s".format(*gyro))
    print("Magnetic      X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} uT".format(*magnetic))
    print("")
    time.sleep(0.5)
    #except Exception as e:
    #    print(e)
    #    time.sleep(1)
        