#!/usr/bin/python
# ***************************************************************************
#   I2CPythonMints
#   ---------------------------------
#   Written by: Lakitha Omal Harindha Wijeratne
#   - for -
#   MINTS :  Multi-scale Integrated Sensing and Simulation
#     & 
#   TRECIS: Texas Research and Education Cyberinfrastructure Services
#
#   ---------------------------------
#   Date: July 7th, 2022
#   ---------------------------------
#   This module is written for generic implimentation of MINTS projects
#   --------------------------------------------------------------------------
#   https://github.com/mi3nts
#   https://trecis.cyberinfrastructure.org/
#   http://utdmints.info/
#  ***************************************************************************



import sys
import time
import os
import smbus2
#from i2cMints.i2c_scd30 import SCD30
from i2cMints.i2c_bme280 import BME280
from i2cMints.i2c_bno080 import BNO080
from mintsXU4 import mintsSensorReader as mSR

debug        = False 
bus          = smbus2.SMBus(5)

#  BME280
bme280       = BME280(bus,debug)

# BNO080
bno080       = BNO080(bus,debug) 



checkTrials  = 0
loopInterval = 5 


def main(loopInterval):
    global checkTrials, checkCurrent 
    bme280_valid   = bme280.initiate(30)
    startTime    = time.time()
    while True:
        try:
            print("======= BME280 ========")
            if bme280_valid:
                mSR.BME280WriteI2c(bme280.read())
            print("=======================")
            time.sleep(2)       
            startTime = mSR.delayMints(time.time() - startTime,loopInterval)
            
        except Exception as e:
            print(e)
            time.sleep(10)
        
if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring Climate data for MASK")
    main(loopInterval)