import smbus2
import time

# TMP117 I2C address
TMP117_ADDRESS = 0x48




# Register addresses
TMP117_TEMP_RESULT = 0x00  # Temperature result register

TMP117_DEVICE_ID   = 0x0F

TMP117_SERIAL_NUM_1 = 0x05 # Serial number part 1
TMP117_SERIAL_NUM_2 = 0x06 # Serial number part 2
TMP117_SERIAL_NUM_3 = 0x08 # Serial number part 2


# Create an I2C bus object
bus = smbus2.SMBus(4)  # 1 is the I2C bus number on Raspberry Pi; change as needed for your platform

def read_temperature():
    # Read 2 bytes from the temperature result register
    data = bus.read_i2c_block_data(TMP117_ADDRESS, TMP117_TEMP_RESULT, 2)

    # Convert the data to temperature in Celsius
    temp_raw = (data[0] << 8) | data[1]
    temp_celsius = temp_raw * 0.0078125

    return temp_celsius

def read_serial_number():
    # Read 2 bytes from SERIAL_NUM_1 register (0xFE)
    serial_num1_data = bus.read_i2c_block_data(TMP117_ADDRESS, TMP117_SERIAL_NUM_1, 2)
    # Read 2 bytes from SERIAL_NUM_2 register (0xFF)
    serial_num2_data = bus.read_i2c_block_data(TMP117_ADDRESS, TMP117_SERIAL_NUM_2, 2)
    
    
    serial_num3_data = bus.read_i2c_block_data(TMP117_ADDRESS, TMP117_SERIAL_NUM_3, 2)

    # Combine the data to form the 32-bit serial number
    serial_num = (
        (serial_num1_data[0] << 8 | serial_num1_data[1]) << 32 | 
        (serial_num2_data[0] << 8 | serial_num2_data[1]) << 16 | 
        (serial_num3_data[0] << 8 | serial_num3_data[1])
    )

    combined_id = bytearray(
            [
                serial_num1_data[0],
                serial_num1_data[1],
                serial_num2_data[0],
                serial_num2_data[1],
                serial_num3_data[0],
                serial_num3_data[1],
            ]
        )
    
    print(convert_to_integer(combined_id))
    return serial_num

  
def read_device_id():
    device_id_data = bus.read_i2c_block_data(TMP117_ADDRESS, TMP117_DEVICE_ID, 2)
    
    # Combine the data to form the 16-bit device ID
    device_id = (device_id_data[0] << 8) | device_id_data[1]
    
    return device_id
    
  
def convert_to_integer(bytes_to_convert: bytearray) -> int:
    """Use bitwise operators to convert the bytes into integers."""
    integer = None
    for chunk in bytes_to_convert:
        if not integer:
            integer = chunk
        else:
            integer = integer << 8
            integer = integer | chunk
    return integer
  
def main():
    try:
        # Read the serial number of the TMP117 sensor
        serial_number = read_serial_number()
        print(f"TMP117 Serial Number: 0x{serial_number:08X}")
        print(serial_number)
        
        device_id_data = read_device_id()
        #print(f"TMP117 Device ID: 0x{device_id_data:08X}")
        print(device_id_data)
        
        
        while True:
            # Read temperature
            temperature = read_temperature()
            print(f"Temperature: {temperature:.2f} °C")

            # Wait for a second before reading the temperature again
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted by user")

    # Close the I2C bus
    bus.close()

if __name__ == "__main__":
    main()
