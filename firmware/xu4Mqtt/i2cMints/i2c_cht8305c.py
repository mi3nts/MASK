import datetime
from datetime import timedelta
import logging
from smbus2 import SMBus, i2c_msg
import struct
import time
import math
# Datasheet: https://dfimg.dfrobot.com/nobody/wiki/4c8e1057e1c118e5c72f8ff6147575db.pdf

CHT8305C_I2C_ADDR         = 0x40
CHT8305C_REG_MANUFACTURER = 0xFE
CHT8305C_REG_VERSION      = 0xFF
CHT8305C_REG_TEMPERUTURE  = 0x00
CHT8305C_REG_HUMIDITY     = 0x01


class CHT8305C:
    def __init__(self, i2c_dev,debugIn):
        self.i2c_addr  = CHT8305C_I2C_ADDR
        self.i2c       = i2c_dev
        self.debug     = debugIn

    def initiate(self):
        print("============== CHT8305C I2C ==============")
        time.sleep(1)
        try:
            self.i2c.read_byte(CHT8305C_I2C_ADDR) 
            print("CHT8305C sensor connected")
            time.sleep(1)
            print(f"Manufacturer: {self.getManufacturer()}")
            time.sleep(1)
            print(f"Version ID: {self.getVersionID()}")
            time.sleep(1)
            return True;
        except Exception as e:
            time.sleep(0.01)
            print(f"Error reading I2C: {e}")
            print("CHT8305C sensor not found")
            return False




    def readI2c(self, registerIn, replySize):
        # Command is  the register requested

        try:
            # Send command to the I2C device
            self.i2c.write_byte(\
                                CHT8305C_I2C_ADDR,\
                                registerIn);
            # Delay for the I2C response
            time.sleep(.2)
    
            # Delay for the I2C response
            receivedBytes = i2c_msg.read(\
                                        CHT8305C_I2C_ADDR,\
                                        replySize)
            
            self.i2c.i2c_rdwr(receivedBytes)

            
            outPut = list(receivedBytes)

        except Exception as e:
            time.sleep(0.01)
            print(f"Error reading I2C: {e}")

        return outPut;

    def getManufacturer(self):
        manufacturerID = self.readI2c(CHT8305C_REG_MANUFACTURER, 2)
        if manufacturerID is None:
            print("Failed to read manufacturer ID from sensor.")
            return None
        return manufacturerID

    def getVersionID(self):
        versionID = self.readI2c(CHT8305C_REG_VERSION, 2)
        if versionID is None:
            print("Failed to read version ID.")
            return None
        return versionID


    def getTemperatureAndHumidity(self):
        climateData = self.readI2c(CHT8305C_REG_TEMPERUTURE, 4)
        if climateData is None:
            print("Failed to read version clinmate data.")
            return None
        return climateData



    def calculateDewPoint(self,temperature, humidity):
        # Applying the Magnus-Tetens approximation formula for dew point
        dew_point = 243.04 * (math.log(humidity / 100.0) + ((17.625 * temperature) / (243.04 + temperature))) / \
                    (17.625 - math.log(humidity / 100.0) - ((17.625 * temperature) / (243.04 + temperature)))
        return dew_point


    def read(self):
        # Read PC data
        dateTime  = datetime.datetime.now() 
        
        climateData = self.getTemperatureAndHumidity()

        # Combine the bytes to form the 16-bit data values
        temperaturePre  = climateData[0] << 8 | climateData[1]  # Combine the first two bytes for temperature
        humidityPre     = climateData[2] << 8 | climateData[3]  # Combine the next two bytes for humidity

        # Calculate temperature using the formula
        temperature = (float(temperaturePre) * 165 / 65535.0) - 40.0

        # Calculate humidity using the formula
        humidity    = (float(humidityPre) / 65535.0) * 100

        dewPoint = self.calculateDewPoint(temperature,humidity)


        return [dateTime, \
                  temperature,\
                  humidity,
                  dewPoint]

