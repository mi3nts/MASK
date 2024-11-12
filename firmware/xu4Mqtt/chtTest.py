import smbus
import time

# Open the I2C bus (bus 5 in this case)
bus = smbus.SMBus(5)

# Device address (0x40)
device_address = 0x40

# Number of bytes to read (we can read up to 256 bytes at a time)
num_bytes = 256

# Read bytes from the device (starting from register 0x00)
try:
    # Read block of data from the device (starting from register 0x00)
    data = bus.read_i2c_block_data(device_address, 0x00, num_bytes)
    
    # Print data in a format similar to i2cdump
    print("     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef")
    for i in range(0, num_bytes, 16):
        # Display the hex values in rows, 16 bytes per row
        hex_values = " ".join(f"{x:02x}" for x in data[i:i+16])
        ascii_values = "".join([chr(x) if 32 <= x <= 126 else '.' for x in data[i:i+16]])
        print(f"{i:02x}: {hex_values:<47} {ascii_values}")
except IOError as e:
    print(f"Error reading from I²C device: {e}")
