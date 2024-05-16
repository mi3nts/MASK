# # 
# Firmware adapted from https://github.com/RequestForCoffee/scd30
import datetime
from datetime import timedelta
import logging
import smbus2
import struct
import time
from math import atan2, sqrt, pi


from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
    BNO_REPORT_LINEAR_ACCELERATION,
    BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR,
    BNO_REPORT_GAME_ROTATION_VECTOR,
    BNO_REPORT_STEP_COUNTER,
    BNO_REPORT_STABILITY_CLASSIFIER,
    BNO_REPORT_ACTIVITY_CLASSIFIER,
    BNO_REPORT_SHAKE_DETECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_extended_bus import ExtendedI2C as I2C


# # to_s16 = lambda x: (x + 2**15) % 2**16 - 2**15
# # to_u16 = lambda x: x % 2**16

# BME280_I2C_ADDR = 0x77
mapping  =  {
                'Unknown': 0,
                'In-Vehicle': 1,
                'On-Bicycle': 2,
                'On-Foot': 3,
                'Still': 4,
                'Tilting': 5,
                'Walking': 6,
                'Running': 7,
                'OnStairs': 8
            }


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
                self.bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)
                self.bno.enable_feature(BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)
                self.bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR)
                self.bno.enable_feature(BNO_REPORT_STEP_COUNTER)
                self.bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)
                self.bno.enable_feature(BNO_REPORT_ACTIVITY_CLASSIFIER)
                self.bno.enable_feature(BNO_REPORT_SHAKE_DETECTOR)

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
        
    def find_heading(self,dqw, dqx, dqy, dqz):
        norm = sqrt(dqw * dqw + dqx * dqx + dqy * dqy + dqz * dqz)
        dqw = dqw / norm
        dqx = dqx / norm
        dqy = dqy / norm
        dqz = dqz / norm

        ysqr = dqy * dqy

        t3 = +2.0 * (dqw * dqz + dqx * dqy)
        t4 = +1.0 - 2.0 * (ysqr + dqz * dqz)
        yaw_raw = atan2(t3, t4)
        yaw = yaw_raw * 180.0 / pi
        if yaw > 0:
            yaw = 360 - yaw
        else:
            yaw = abs(yaw)
        return yaw  # heading in 360 clockwise
    

    def activity_classification_summary(self,activity_classification):
        most_likely     = activity_classification["most_likely"]
        mostLikelyIndex = mapping.get(activity_classification['most_likely'], -1) 
        mostLikelyConf  = activity_classification[most_likely]
        outPut          = [ mostLikelyIndex,\
                            mostLikelyConf,\
                            activity_classification["Unknown"], \
                            activity_classification["In-Vehicle"], \
                            activity_classification["On-Bicycle"], \
                            activity_classification["On-Foot"], \
                            activity_classification["Still"], \
                            activity_classification["Tilting"], \
                            activity_classification["Walking"], \
                            activity_classification["Running"], \
                            activity_classification["OnStairs"], \
                        ]
        return outPut;

    def shake_summary(self,shake_output):
        if shake_output == False:
            return 0
        
        return 1; 


    def read(self):
        try:
            dateTime                                            = datetime.datetime.now() 
            accel_x, accel_y, accel_z                           = self.bno.acceleration  # pylint:disable=no-member
            gyro_x, gyro_y, gyro_z                              = self.bno.gyro  # pylint:disable=no-member
            mag_x, mag_y, mag_z                                 = self.bno.magnetic  # pylint:disable=no-member
            quat_i, quat_j, quat_k, quat_real                   = self.bno.quaternion  # pylint:disable=no-member
            linear_accel_x,linear_accel_y, linear_accel_z       = self.bno.linear_acceleration
            geo_quat_i,geo_quat_j,geo_quat_k,geo_quat_real      = self.bno.geomagnetic_quaternion
            heading                                             = self.find_heading(quat_real, quat_i, quat_j, quat_k)
            heading_geo                                         = self.find_heading(geo_quat_real, geo_quat_i, geo_quat_j, geo_quat_k)
            game_quat_i,game_quat_j, game_quat_k,game_quat_real = self.bno.game_quaternion 
            steps                                               = self.bno.steps
            shake                                               = self.shake_summary(self.bno.shake)

            [ mostLikelyIndex,\
                            mostLikelyConf,\
                            unknown, \
                            in_vehicle, \
                            on_bicycle, \
                            on_foot, \
                            still, \
                            tilting, \
                            walking, \
                            running, \
                            on_stairs \
                        ]                                        = self.bno.activity_classification


            return [dateTime,\
                    accel_x, accel_y, accel_z,\
                    gyro_x, gyro_y, gyro_z,\
                    mag_x, mag_y, mag_z,\
                    quat_i, quat_j, quat_k, quat_real,\
                    linear_accel_x,linear_accel_y, linear_accel_z,\
                    geo_quat_i,geo_quat_j,geo_quat_k,geo_quat_real,\
                    heading,
                    heading_geo,
                    game_quat_i,game_quat_j, game_quat_k,game_quat_real,
                    steps ,\
                    shake,\
                    mostLikelyIndex,\
                    mostLikelyConf,\
                    unknown, \
                    in_vehicle, \
                    on_bicycle, \
                    on_foot, \
                    still, \
                    tilting, \
                    walking, \
                    running, \
                    on_stairs\
                  ];
    
        except Exception as e:
            print(e)
            time.sleep(1)
            return [];


