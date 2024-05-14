from periphery import I2C, I2CError
import time


DEVICE_ADDRESS = 0x4A

# Open I2C device
i2c = I2C("/dev/i2c-1")

# Define the list of bytes to write
bytes_to_write =  [0x05, 0x00, 0x01, 0x00, 0x01]  # Example command bytes


#06 00 02 01 F9 00
command2 =  [0x06, 0x00, 0x02, 0x01, 0x01]  # Example command bytes


# Convert the list to a bytearray
bytes_to_write = [0x01, 0x02, 0x03, 0x04]


print("writing to the device")
# Open I2C device

with I2C("/dev/i2c-1") as i2c:
    # Write the bytearray to the device
    messages = I2C.Message(bytearray(bytes_to_write))
    i2c.transfer(DEVICE_ADDRESS, [messages]) 
    time.sleep(.1)
    
    bytes_read = i2c.transfer(DEVICE_ADDRESS, [I2C.Message([0] * 4)])
    print(bytes_read)
    
    # Print the bytes read from the device
    print("Bytes read:", bytes_read)