# ***************************************************************************
#   ips7100I2cReader
#   ---------------------------------
#   Written by: Lakitha Omal Harindha Wijeratne
#   - for -
#   Mints: Multi-scale Integrated Sensing and Simulation
#   ---------------------------------
#   Date: May 3rd, 2024
#   ---------------------------------
#   This module is written for generic implimentation of MINTS projects
#   --------------------------------------------------------------------------
#   https://github.com/mi3nts
#   http://utdmints.info/
#  ***************************************************************************

import datetime
from datetime import timedelta
import logging
import smbus2
import struct
import time



class IpsSensor:
    POLY = 0x8408

    def __init__(self,bus_number):
        self.bus = smbus2.SMBus(bus_number)
        self.pc_values = [0] * 7
        self.pm_values = [0.0] * 7


    def read_i2c(self, command, reply_size):
        received_bytes = []
        received_bytes.clear()

        # Send command to the I2C device
        self.bus.write_byte(0x4B, command)

        # Request `reply_size` bytes from the I2C device
        received_bytes = self.bus.read_i2c_block_data(0x4B, command, reply_size)

        # print("[", end=" ")
        # print(" ".join(f"{byte:02X}" for byte in received_bytes), end=" ")
        # print("]")

        # Calculate the checksum of the received data
        message_checksum = self.get_checksum(received_bytes, reply_size - 2)
        received_checksum = (received_bytes[-2] << 8) + received_bytes[-1]

        if hasattr(self, 'ips_debug') and self.ips_debug:
            print(f"Expected checksum: {message_checksum}, Received checksum: {received_checksum}")

        if message_checksum == received_checksum:
            checksum_pass = True
            print("Checksum passed.")
        else:
            checksum_pass = False
            print("Checksum failed.")
            time.sleep(0.1)
        
        return received_bytes, checksum_pass;


    def get_checksum(self, data, length):
        crc = 0xFFFF
        for j in range(length):
            byte = data[j]
            for i in range(8):
                if (crc & 0x0001) ^ (byte & 0x0001):
                    crc = (crc >> 1) ^ self.POLY
                else:
                    crc >>= 1
                byte >>= 1
        
        # CRC calculation is complete
        # Perform bit reversal
        crc = ~crc
        # Re-arrange the bytes to swap endianness
        crc = ((crc << 8) & 0xFF00) | ((crc >> 8) & 0x00FF)
        return crc
    
    def bytes_to_float(self, byte_data):
            # Convert 4 bytes to float
            # import struct
            return struct.unpack('<f', bytes(byte_data))[0]

    def update(self):
        # Read PC data
        pc_raw_values, checkSumPassedPC = self.read_i2c(0x11, 30)
        pm_raw_values, checkSumPassedPM = self.read_i2c(0x12, 32)
        # Assemble PC values (unsigned long) from 4 bytes using bitwise operations
        time.sleep(0.1)
        for i in range(7):
            self.pc_values[i] = (pc_raw_values[(i * 4) + 3] |
                                 (pc_raw_values[(i * 4) + 2] << 8) |
                                 (pc_raw_values[(i * 4) + 1] << 16) |
                                 (pc_raw_values[(i * 4)]) << 24)
        time.sleep(0.1)
        for i in range(7):
            start_idx = i * 4
            float_bytes = pm_raw_values[start_idx:start_idx + 4]
            self.pm_values[i] = self.bytes_to_float(float_bytes)

        return self.pc_values, self.pm_values, checkSumPassedPC, checkSumPassedPM

        # Read PM data
        # Introduce a small delay if necessary (not typically needed in Python with SMBus)
        # import time
        # time.sleep(0.1)
        # Assemble PM values (float) from 4 bytes using struct.unpack
 
    def get_vref(self):
        # Read 4 bytes using the command 0x69 and checksum enabled
        message, checkSumPassed = self.read_i2c(0x69, 4)

        # Convert the received data to an unsigned short integer (16-bit value)
        vref = message[1] | (message[0] << 8)

        return vref, checkSumPassed


    def get_serial_number(self):
        # Read 19 bytes using the command 0x77 and checksum enabled
        serial_data,checkSumPassed = self.read_i2c(0x77, 19)
        
        # Modify the 18th byte to be a null-terminator (set it to 0)
        if len(serial_data) > 17:
            serial_data[17] = 0
        
        return serial_data,checkSumPassed

    def get_version(self):
        # Read 9 bytes using the command 0x78 and checksum enabled
        version_data,checkSumPassed = self.read_i2c(0x78, 9)
        
        # Modify the 8th byte to be a null-terminator (set it to 0)
        if len(version_data) > 7:
            version_data[7] = 0
        
        return version_data,checkSumPassed
    


ips7100      = IpsSensor(3)

loopInterval = 5 


if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Serial Number")
    print(ips7100.get_serial_number())

    print("Version")
    print(ips7100.get_version())
    
    print("VREF")
    print(ips7100.get_vref())

    while True:
        try:
            
            PCData, PMData, PCCS, PMCS =  ips7100.update()        
            print(datetime.datetime.now())
            print("PC Data")
            print(PCData)
            print(" PM Data" )
            print(PMData)
            time.sleep(1)
        except Exception as e:
            # Code to handle any other exception
            print(f"An error occurred: {e}")
          



    