import smbus2
import time
import datetime
import adafruit_icm20x

class ICM20948:

    def __init__(self, i2c_dev,debugIn):
        
        self.i2c      = i2c_dev
        self.debug    = debugIn


    def initiate(self,retriesIn):
        print("============== ICM20948 ==============")        
        ready = None
        while ready is None and retriesIn:
            try:
                self.soft_reset()
                time.sleep(1)

                self.icm20948  = adafruit_icm20x.ICM20948(self.i2c)

                print("ICM20948 Device Initialized to defauls of +-8g and 500 dps:")
                time.sleep(1)
                
            except OSError:
                pass
            time.sleep(1)
            retriesIn -= 1

        if not retriesIn:
            time.sleep(1)
            return False
        
        else:
            print("TMP117 Found")
            time.sleep(1)
            return True       
      
    
    def read(self):
        try:
            dateTime = datetime.datetime.now() 
            self.acceleration =  self.icm20948.acceleration
            self.gyro         =  self.icm20948.gyro
            self.magnetic     =  self.icm20948.magnetic

            print(dateTime)
            print(self.acceleration)
            print(self.gyro)
            print(self.magnetic)

            return [dateTime];
        
        except Exception as e:
        
            time.sleep(1)
            print("An exception occurred:", type(e).__name__, "–", e) 
            return [dateTime];
        