
# Use SMBus2 
# Make sure speed is 400k 
# Check if the device is available 
#   sudo i2cdetect -y 1 
#   The device is available on bus 4 with address 0x4a 

# Try SPI too: 
    # https://github.com/adafruit/Adafruit_CircuitPython_BNO08x/blob/main/examples/bno08x_simpletest_spi.py
# import smbus2

# # Define the I2C bus number
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
    get_pid = [6, 0, 2, 0, 0xF9, 0]
    
    # Send command to request product ID
    # while(True):
        # try:
    bus.write_i2c_block_data(BNO_ADDRESS, 0, get_pid)
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

get_product_id()



# def get_quaternion():
#     cargo = bytearray(23)  # cargo buffer
#     cargo[0] = 23
#     bus.write_i2c_block_data(BNO_ADDRESS, 0, cargo)
#     time.sleep(0.1)  # Delay to allow data to be ready
#     data = bus.read_i2c_block_data(BNO_ADDRESS, 0, 23)
#     return data






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
