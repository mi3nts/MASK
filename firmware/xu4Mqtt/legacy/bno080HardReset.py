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

from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)

debug        = False 
bus          = I2C(4)


time.sleep(1)
bno       =  BNO08X_I2C(bus)

time.sleep(5)
bno.hard_reset()