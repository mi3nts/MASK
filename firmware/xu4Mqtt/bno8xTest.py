import sys
import time
import os
import smbus2
from i2cMints.i2c_bno080 import BNO080
from mintsXU4 import mintsSensorReader as mSR

debug  = False 

bus     = smbus2.SMBus(4)

BNO080  = BNO080(bus)

BNO080.initiate()