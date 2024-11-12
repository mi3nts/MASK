import datetime
from datetime import timedelta
import logging
import smbus2
import struct
import time

CHT8305C_I2C_ADDR           = 0x40
CHT8305C_REG_MANUFACTURER   = 0xFE
CHT8305C_REG_VERSION        = 0xFF

class CHT8305C:
    def __init__(self, i2c_dev,debugIn):
        self.i2c_addr  = CHT8305C_I2C_ADDR
        self.i2c       = i2c_dev
        self.debug     = debugIn

    def initiate(self):
        print("============== CHT8305C I2C ==============")
        if self.is_connected():
            print("CHT8305C sensor connected")
            time.sleep(1)
            print(f"Manufacturer: {self.get_manufacturer()}")
            time.sleep(1)
            print(f"Version ID: {self.get_version_id()}")
            return True
        else:
            print("CHT8305C sensor connection failed")
            return False

    def is_connected(self):
        try:
            self.i2c.write_quick(self.i2c_addr)
            return True
        except IOError:
            return False


    def read_i2c(self, command, reply_size):
        # Command is  the register requested
        received_bytes = []
        try:
            # Send command to the I2C device
            self.i2c.write_byte(
                CHT8305C_I2C_ADDR, command)
            # Delay for the I2C response
            time.sleep(0.01)  
    
            # Delay for the I2C response
            received_bytes = self.i2c.read_i2c_block_data(
                CHT8305C_I2C_ADDR, command, reply_size)
            
        except Exception as e:
            time.sleep(0.01)
            print(f"Error reading I2C: {e}")
        return received_bytes;

    def get_manufacturer(self):
        manufacturer_data = self.read_i2c(CHT8305C_REG_MANUFACTURER, 2)
        if manufacturer_data is None:
            print("Failed to read manufacturer ID from sensor.")
            return None
        manufacturer_id = (manufacturer_data[0] << 8) | manufacturer_data[1]
        return manufacturer_id

    def get_version_id(self):
        version_data = self.read_i2c(CHT8305C_REG_VERSION, 2)
        if version_data is None:
            print("Failed to read version ID.")
            return None
        # Convert the byte data into a 16-bit integer
        version_id = (version_data[0] << 8) | version_data[1]
        return version_id



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

