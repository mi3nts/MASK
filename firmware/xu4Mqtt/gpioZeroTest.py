import time
import board
import busio
from adafruit_bus_device import i2c_device

# Define I2C device address
DEVICE_ADDRESS = 0x4A

# Create I2C bus
i2c_bus = busio.I2C(board.SCL, board.SDA)
bus_device_obj = i2c_device.I2CDevice(i2c_bus, DEVICE_ADDRESS)

# Define packet
packet = bytearray([0x05, 0x00, 0x01, 0x00, 0x01])

# Create buffer to read into
response_buffer = bytearray(4)

# Write packet to device
with bus_device_obj as i2c:
    i2c.write(packet)

# Wait for the data to be ready
time.sleep(0.1)

# Read data into response_buffer
with bus_device_obj as i2c:
    i2c.readinto(response_buffer)

print(response_buffer)
