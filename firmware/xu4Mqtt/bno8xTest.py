# import sys
# import time
# import os
# import smbus2
# from i2cMints.i2c_bno080 import BNO080
# from mintsXU4 import mintsSensorReader as mSR

# debug  = False 

# bus     = smbus2.SMBus(4)

# BNO080  = BNO080(bus)

# BNO080.initiate()


#  Just for soft reset 


import time
from smbus2 import SMBus, i2c_msg

# Constants
CHANNEL_EXECUTABLE = 1  # Channel for executing commands
RESET_COMMAND = 1  # Reset command
DELAY_INTERVAL = 0.05  # 50 milliseconds (0.05 seconds)

def soft_reset(bus: SMBus, device_address: int):
    # Send reset command
    shtp_data = [RESET_COMMAND]  # Reset command
    # Create an I2C message to write data to the sensor
    write_msg = i2c_msg.write(device_address, [CHANNEL_EXECUTABLE] + shtp_data)
    bus.i2c_rdwr(write_msg)
    
    # Delay for 50 milliseconds
    time.sleep(DELAY_INTERVAL)
    
    # Flush the incoming data
    while receive_packet(bus, device_address):
        pass
    
    # Delay again for another 50 milliseconds
    time.sleep(DELAY_INTERVAL)
    
    # Flush any remaining incoming data
    while receive_packet(bus, device_address):
        pass

def receive_packet(bus: SMBus, device_address: int):
    # Read packet from the sensor (4 bytes for header + data)
    read_msg = i2c_msg.read(device_address, 4)
    bus.i2c_rdwr(read_msg)
    
    # Process the incoming data
    header = list(read_msg)  # Convert I2C message to a list
    
    # If no data available, return False
    if not header:
        return False
    
    # Calculate data length from header
    packet_length = header[0] | (header[1] << 8)
    data_length = packet_length - 4  # Subtract header length
    
    if data_length > 0:
        # Read the remaining data bytes
        data_read_msg = i2c_msg.read(device_address, data_length)
        bus.i2c_rdwr(data_read_msg)
        data = list(data_read_msg)
        print(data)
        # Process incoming data (if needed)
        # Example: print(data)
        
    # Return True if data was received and processed
    return True

# Example usage:
# Initialize SMBus
bus_number = 4 # Specify the correct I2C bus number for your setup
device_address = 0x4A  # Specify the correct I2C device address (0x4A or 0x4B)

# Initialize the SMBus instance
bus = SMBus(bus_number)

# Call soft reset function
soft_reset(bus, device_address)

# Close the SMBus when done
bus.close()