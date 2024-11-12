import datetime
from datetime import timedelta
import logging
import smbus2
import struct
import time

CHT8305C_I2C_ADDR = 0x40

class CHT8305C:

    def __init__(self, i2c_dev,debugIn):
        
        self.i2c_addr  = CHT8305C_I2C_ADDR
        self.i2c       = i2c_dev
        self.debug     = debugIn

    def initiate(self,retriesIn):
        print("============== CHT8305C I2C ==============")
        return True

    def read_i2c(self, command, reply_size):
        # Command is  the register requested
        received_bytes = []
        received_bytes.clear()

        # Send command to the I2C device
        self.i2c.write_byte(
            CHT8305C_I2C_ADDR, command)
        
        # Delay for the I2C response
        time.sleep(0.01)  
        
        # Delay for the I2C response
        received_bytes = self.i2c.read_i2c_block_data(
            CHT8305C_I2C_ADDR, command, reply_size)

        time.sleep(0.01)
        return received_bytes;

    def read(self):
        # Read PC data
        dateTime  = datetime.datetime.now() 
        rawValues = self.read_i2c(0x00, 4)

        if rawValues is None:
            return [];

        # Convert the data into two 16-bit integers
        temperatureRaw = (rawValues[0] << 8) | rawValues[1]
        humidityRaw    = (rawValues[2] << 8) | rawValues[3]

        time.sleep(0.1)

        temperature = ((float(temperatureRaw) * 165 / 65535.0) - 40.0)
        humidity    = ((float(humidityRaw) / 65535.0) * 100)
    
        return [dateTime, \
                  temperature,\
                  humidity]

