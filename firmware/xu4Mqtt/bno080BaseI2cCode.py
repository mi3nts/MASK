
# Use SMBus2 
# Make sure speed is 400k 
# Check if the device is available 
#   sudo i2cdetect -y 1 
#   The device is available on bus 4 with address 0x4a 

# Try SPI too: 
    # https://github.com/adafruit/Adafruit_CircuitPython_BNO08x/blob/main/examples/bno08x_simpletest_spi.py
# import smbus2

# Define the I2C bus number
# bus_number = 4  # Adjust according to your setup
import smbus2
import time

# I2C address of BNO080
BNO_ADDRESS = 0x4A

# Configuration parameters
plot_interval = 1  # plot interval in seconds
reporting_frequency = 400  # reporting frequency in Hz

# Function to read quaternion data

# Initialize I2C bus
bus = smbus2.SMBus(4, 400000)  # Assuming you're using /dev/i2c-4

# Function to check for devices on the I2C bus
def detect_devices(bus):
    devices = []
    for address in range(128):  # I2C addresses range from 0x00 to 0x7F
        try:

            print("AD" + str(address))
            print(bus.read_byte(address))
            devices.append(address)
            
        except OSError:
            pass
    return devices


def get_product_id():
    # Define command to request product ID
    get_pid = [0x06, 0x00, 0x02, 0x00, 0xF9, 0x00]
    
    # Send command to request product ID
    # while(True):
        # try:
    for byte in get_pid:
        bus.write_byte(BNO_ADDRESS, byte)
            # break
        # except Exception as e:
        #     # Print the error message if an exception occurs
        #     print("Error:", e)
    print("Written to Device")
    time.sleep(0.2)  # Wait for response

    # Read response
    while True:
        try:
            response = [bus.read_byte(BNO_ADDRESS) for _ in range(25)]
        
            if response[4] == 0xF8:  # Check for command response
                break
        except Exception as e:
            # Print the error message if an exception occurs
            print("Error:", e)
        time.sleep(0.1)  # Wait for response
        
    # Parse response and print product ID
    reset_cause = response[5]
    sw_major = response[6]
    sw_minor = response[7]
    print("Product ID response:")
    print("Reset cause:", hex(reset_cause))
    print("SW Major:", hex(sw_major))
    print("SW Minor:", hex(sw_minor))


def read_shtp_advertising(bus, address):

    """
    Reads SHTP advertising data from the BNO080 sensor.

    Parameters:
    - bus: An instance of the SMBus class representing the I2C bus.
    - address: The I2C address of the BNO080 sensor.

    Returns:
    - advertising_data: A list containing the SHTP advertising data.
    """
    advertising_data = []

    # Send start condition
    bus.write_byte(address, 1)

    # Repeat until length is still greater than 0
    while True:
        # Request advertising data from BNO080
        advertising_data += bus.read_i2c_block_data(address, 0, 32)

        # Check if length is still greater than 0
        if advertising_data[0] == 0:
            break

    # Print the advertising data
    print("SHTP advertising:", end=" ")
    for byte in advertising_data[4:]:  # Skip the first 4 bytes
        print(hex(byte), end=", ")
    print()

    return advertising_data

# get_product_id()

# read_shtp_advertising(bus, BNO_ADDRESS)

# def get_quaternion():
#     cargo = bytearray(23)  # cargo buffer
#     cargo[0] = 23
#     bus.write_i2c_block_data(BNO_ADDRESS, 0, cargo)
#     time.sleep(0.1)  # Delay to allow data to be ready
#     data = bus.read_i2c_block_data(BNO_ADDRESS, 0, 23)
#     return data



address    = 0x4A  # Example device address (BNO080)
block_size = 32    # Example block size for reading data

while True:
    try:
        # Attempt to initiate communication with the device
        bus.write_byte(BNO_ADDRESS, 0)  # Sending a dummy byte to check device presence
        break  # Exit the loop if communication is successful
    except OSError as e:
        pass  # Device not found, retrying...


# Device found, print a message
print("BNO found")


# # Define a list to store the cargo data
# cargo = [0] * 32

# #  print("End of SHTP advertising")
# print(bus.read_byte(BNO_ADDRESS))
# print(bus.read_byte_data(BNO_ADDRESS,0))

# Send an SHTP command to request data
command =  [0x06, 0x00, 0x02, 0x00, 0xF9, 0x00]  # Example command bytes

reversed_list = command[::-1]

bus.write_i2c_block_data(BNO_ADDRESS, 0, reversed_list)

print("Bytes Written")

# Wait for a short time for the sensor to process the command

time.sleep(0.1)

# Receive response from the sensor
num_bytes = 10 

response = []

for _ in range(num_bytes):
    byte = bus.read_byte(BNO_ADDRESS)
    response.append(byte)

print(response)


# Read data from the device

# data = bus.read_byte(address)
# print("Data received:", data)


# # Main loop
# # while True:
# #     start_time = time.time()
    
# #     # Get quaternion data
# #     quaternion_data = get_quaternion()
    
# #     # Process quaternion data
# #     # Add your processing logic here
    
# #     # Calculate loop duration
# #     loop_duration = time.time() - start_time
    
# #     # Wait to maintain desired reporting frequency
# #     time_to_sleep = max(0, 1.0/reporting_frequency - loop_duration)
# #     time.sleep(time_to_sleep)
