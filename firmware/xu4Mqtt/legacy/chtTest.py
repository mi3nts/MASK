import smbus2
import time

# Open the I2C bus (bus 5 in this case)
bus = smbus2.SMBus(5)

# Device address (0x40)
device_address = 0x40

# Maximum number of registers (0x00 to 0xFF)
num_registers = 256

# Read all registers one by one
try:
    print("Register  Data")
    for reg in range(num_registers):
        # Read 1 byte from each register
        data = bus.read_byte_data(device_address, reg)
        
        # Print register and corresponding data
        print(f"0x{reg:02X}    0x{data:02X}")

except IOError as e:
    print(f"Error reading from I²C device: {e}")
