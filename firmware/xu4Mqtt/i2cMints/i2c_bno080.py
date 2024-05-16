# # 
# Firmware adapted from https://github.com/RequestForCoffee/scd30
import datetime
from datetime import timedelta
import logging
import smbus2
import struct
import time

from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_extended_bus import ExtendedI2C as I2C







# # to_s16 = lambda x: (x + 2**15) % 2**16 - 2**15
# # to_u16 = lambda x: x % 2**16

# BME280_I2C_ADDR = 0x77

class BNO080:

    def __init__(self, i2c_dev,debugIn):
        
        # self.i2c_addr = BME280_I2C_ADDR
        self.i2c      = i2c_dev
        self.debug    = debugIn

    def initiate(self,retriesIn):
        ready = None
        while ready is None and retriesIn:
            try:
                self.bno = BNO08X_I2C(self.i2c)
                self.bno.enable_feature(BNO_REPORT_ACCELEROMETER)
                self.bno.enable_feature(BNO_REPORT_GYROSCOPE)
                self.bno.enable_feature(BNO_REPORT_MAGNETOMETER)
                self.bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
                ready = True
                
            except OSError:
                pass
            time.sleep(1)
            retriesIn -= 1

        if not retriesIn:
            time.sleep(1)
            print("BNO080 Not Found")
            return False
        
        else:
            print("BNO080 Found")
            time.sleep(1)
            return True       
      
    def read(self):
        try:
            dateTime                          = datetime.datetime.now() 
            accel_x, accel_y, accel_z         = self.bno.acceleration  # pylint:disable=no-member
            gyro_x, gyro_y, gyro_z            = self.bno.gyro  # pylint:disable=no-member
            mag_x, mag_y, mag_z               = self.bno.magnetic  # pylint:disable=no-member
            quat_i, quat_j, quat_k, quat_real = self.bno.quaternion  # pylint:disable=no-member
            return [dateTime,\
                    accel_x, accel_y, accel_z,\
                    gyro_x, gyro_y, gyro_z,\
                    mag_x, mag_y, mag_z,\
                    quat_i, quat_j, quat_k, quat_real\
                    ];
        except Exception as e:
            print(e)
            time.sleep(1)
            return [];


