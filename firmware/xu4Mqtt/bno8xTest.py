import sys
import time
import os
import smbus2
from i2cMints.i2c_scd30 import SCD30
from i2cMints.i2c_bme280 import BME280
from i2cMints.i2c_bno080 import BNO080
from mintsXU4 import mintsSensorReader as mSR

debug  = False 

bus     = smbus2.SMBus(5)


