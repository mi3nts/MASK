import smbus2
import time
from smbus2 import SMBus, i2c_msg



address  = 0x40  # I2C device address
register = 0x00 

bus_num  = 5     # I2C bus number

# Open the I²C bus
with SMBus(bus_num) as bus:
  
    # Write the register to read the first byte
    bus.write_byte(address, 0xFF);
    time.sleep(.2)
    
    # Now read 2 bytes from register 0x00
    read_msg = i2c_msg.read(address, 4)  # Read 2 bytes
    bus.i2c_rdwr(read_msg)  # Send the read message

    
    
    data = list(read_msg)
    first_byte = data[0]
    second_byte = data[1]
    third_byte = data[2]
    fourth_byte = data[3]    
    print(f"First Byte: {first_byte}")
    print(f"Second Byte: {second_byte}")
    print(f"First Byte: {third_byte}")
    print(f"Second Byte: {fourth_byte}")    