import smbus2
import time

# Define I2C device address
DEVICE_ADDRESS = 0x4A

# Create an smbus object
bus = smbus2.SMBus(1)  # 1 indicates /dev/i2c-1, for older Raspberry Pi use 0 for /dev/i2c-0

# Function to send a command packet to the sensor hub


def send_command_packet(command, data):
    # Construct the command packet (header + command + data)
    packet = [0xAA, 0xBB, command] + data  # Example header bytes 0xAA, 0xBB

    # Send the packet to the sensor hub
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0, packet)

# Function to receive a response packet from the sensor hub
def receive_response_packet():
    # Read the response packet from the sensor hub
    response_packet = bus.read_i2c_block_data(DEVICE_ADDRESS, 0, 8)  # Example: Read 8 bytes of data

    return response_packet

# Example usage
packet =  [0x05, 0x00, 0x01, 0x00, 0x01]
bus.write_i2c_block_data(DEVICE_ADDRESS, 0, packet)
time.sleep(0.1)
response_length = bus.read_byte(DEVICE_ADDRESS)
print(response_length)

# Wait for the sensor hub to process the command and prepare response
time.sleep(0.1)
packet =  [0x05, 0x00, 0x01, 0x01, 0x01]
bus.write_i2c_block_data(DEVICE_ADDRESS, 0, packet)
time.sleep(0.1)
response_length = bus.read_byte(DEVICE_ADDRESS)
print(response_length)

time.sleep(0.1)
packet =  [0x06, 0x00, 0x02, 0x01, 0xF9 , 0x00]
bus.write_i2c_block_data(DEVICE_ADDRESS, 0, packet)
time.sleep(0.1)
response_length = bus.read_byte(DEVICE_ADDRESS)
print(response_length)

num_bytes_to_read = 4  # Example: read 4 bytes
data_read = bus.read_i2c_block_data(DEVICE_ADDRESS, 0, num_bytes_to_read)

print(data_read)