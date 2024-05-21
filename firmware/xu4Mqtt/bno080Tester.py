
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
from adafruit_extended_bus import ExtendedI2C as I2C
from adafruit_bno08x.i2c import BNO08X_I2C

from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
    BNO_REPORT_LINEAR_ACCELERATION,
    BNO_REPORT_STEP_COUNTER,
    BNO_REPORT_STABILITY_CLASSIFIER,
    BNO_REPORT_ACTIVITY_CLASSIFIER,
    BNO_REPORT_SHAKE_DETECTOR,
)



def enabler(i2c):
    try: 
  	    bno     = BNO08X_I2C(i2c)
        bno.enable_feature(BNO_REPORT_ACCELEROMETER)    
        bno.enable_feature(BNO_REPORT_GYROSCOPE)
        bno.enable_feature(BNO_REPORT_MAGNETOMETER)
        bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
        bno.enable_feature(BNO_REPORT_STEP_COUNTER)
        bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)
        bno.enable_feature(BNO_REPORT_ACTIVITY_CLASSIFIER)
        bno.enable_feature(BNO_REPORT_SHAKE_DETECTOR)
        return bno, True 
      
    except Exception as e:
        print(f"Something may be wrong with the BNO080: {e}")
        time.sleep(10)
        print("BNO080 Not Found")
        return [], False    
    




i2c     = I2C(4)


for i in range(5):
    bno, enabled  = enabler(i2c)
    if enabled:
        time.sleep(5)
        break;
    if i==5:
        print("BNO Not found")
        exit()
    
    
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