import smbus2
import time
import datetime
# TMP117 I2C address
TMP117_ADDRESS = 0x48

# Register addresses
TMP117_TEMP_RESULT = 0x00  # Temperature result register

TMP117_DEVICE_ID   = 0x0F

TMP117_SERIAL_NUM_1 = 0x05 # Serial number part 1
TMP117_SERIAL_NUM_2 = 0x06 # Serial number part 2
TMP117_SERIAL_NUM_3 = 0x08 # Serial number part 2


# Register addresses
TMP117_CONFIG_REGISTER = 0x01  # Configuration register

MODE_BITS_MASK         = 0b11 << 10  # MODE bits (bits 11 and 10)

CONTINUOUS_MODE        = 0b00 << 10

# Bit masks for the configuration register
CONV_BITS_MASK         = 0b111 << 7  # CONV bits (bits 5 and 6)

# Conversion cycle times (define these constants as needed)
CONV_CYCLE_15_5_MS      = 0b000 << 7
CONV_CYCLE_125_MS       = 0b001 << 7
CONV_CYCLE_250_MS       = 0b010 << 7
CONV_CYCLE_500_MS       = 0b011 << 7
CONV_CYCLE_1000_MS      = 0b100 << 7
CONV_CYCLE_4000_MS      = 0b101 << 7
CONV_CYCLE_8000_MS      = 0b110 << 7
CONV_CYCLE_16000_MS     = 0b111 << 7

# Bit masks for the configuration register
AVERAGE_WITH_MASK      = 0b11 << 5  #   bits (bits 5 and 6)

AVERAGE_WITH_0_POINTS  = 0b00 << 5
AVERAGE_WITH_8_POINTS  = 0b01 << 5
AVERAGE_WITH_32_POINTS = 0b10 << 5
AVERAGE_WITH_64_POINTS = 0b11 << 5

SOFT_RESET_MASK        = 0b1 << 1  #   bits (bits 5 and 6)
SOFT_RESET_VALUE       = 0b0 << 1


# Bit masks
DR_BIT_MASK = 0b1 << 13  # Data ready bit (bit 3)


# Create an I2C bus object
bus = smbus2.SMBus(5)  # 1 is the I2C bus number on Raspberry Pi; change as needed for your platform

def read_temperature():
    # Read 2 bytes from the temperature result register
    data = bus.read_i2c_block_data(TMP117_ADDRESS, TMP117_TEMP_RESULT, 2)

    # Convert the data to temperature in Celsius
    temp_raw = (data[0] << 8) | data[1]
    temp_celsius = temp_raw * 0.0078125

    return temp_celsius

def read_serial_number():
    
    serial_num1_data = bus.read_i2c_block_data(TMP117_ADDRESS, TMP117_SERIAL_NUM_1, 2)
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


def set_continuous_conversion_mode():
    # Read the current value of the configuration register
    config = bus.read_word_data(TMP117_ADDRESS, TMP117_CONFIG_REGISTER)
    
    # Clear the MODE bits and set them to continuous conversion mode
    config = (config & ~MODE_BITS_MASK) | CONTINUOUS_MODE
    
    # Write the updated configuration back to the register
    bus.write_word_data(TMP117_ADDRESS, TMP117_CONFIG_REGISTER, config)
    
    print("TMP117 set to continuous conversion mode.")


def set_conversion_cycle_time(conv_cycle):
    # Read the current value of the configuration register
    config = bus.read_word_data(TMP117_ADDRESS, TMP117_CONFIG_REGISTER)
    
    # Clear the CONV bits and set them to the specified conversion cycle time
    config = (config & ~CONV_BITS_MASK) | conv_cycle
    
    # Write the updated configuration back to the register
    bus.write_word_data(TMP117_ADDRESS, TMP117_CONFIG_REGISTER, config)
    
    print(f"TMP117 conversion cycle time set to: {conv_cycle >> 10}.")


def set_averaged_times(average_times):
    # Read the current value of the configuration register
    config = bus.read_word_data(TMP117_ADDRESS, TMP117_CONFIG_REGISTER)
    
    # Clear the MODE bits and set them to the specified averaging mode
    config = (config & ~AVERAGE_WITH_MASK) | average_times
    
    # Write the updated configuration back to the register
    bus.write_word_data(TMP117_ADDRESS, TMP117_CONFIG_REGISTER, config)
    
    print(f"TMP117 set to mode: {average_times >> 10}.")



def soft_reset():
    # Write the soft reset value to the configuration register
    config = bus.read_word_data(TMP117_ADDRESS, TMP117_CONFIG_REGISTER)
    
    # Clear the MODE bits and set them to the specified averaging mode
    config = (config & ~SOFT_RESET_MASK) | SOFT_RESET_VALUE 
    
    # Write the updated configuration back to the register
    bus.write_word_data(TMP117_ADDRESS, TMP117_CONFIG_REGISTER, config)
    
    print("Software Reset")

def get_data_ready():

    config = bus.read_word_data(TMP117_ADDRESS, TMP117_CONFIG_REGISTER)

    # Check the data ready bit
    # print(config & DR_BIT_MASK)
    return config & DR_BIT_MASK



def main():
    try:
        # Read the serial number of the TMP117 sensor
        soft_reset()
        time.sleep(1)
        read_serial_number()
        time.sleep(1)
        print("TMP117 Serial Number:")
        print(tmp117.serial_number())
        time.sleep(1)
        device_id_data = self.read_device_id()
        #print(f"TMP117 Device ID: 0x{device_id_data:08X}")
        print(device_id_data)
        time.sleep(1)
        set_continuous_conversion_mode()
        time.sleep(1)
        set_conversion_cycle_time(CONV_CYCLE_1000_MS)
        time.sleep(1)
        set_averaged_times(AVERAGE_WITH_8_POINTS)
        time.sleep(1)

        while True:
            # Read temperature
            if( get_data_ready()):
                print(datetime.datetime.now())
                temperature = read_temperature()
                print(f"Temperature: {temperature:.2f} °C")
            else:
                time.sleep(.1)
            # Wait for a second before reading the temperature again
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted by user")

    # Close the I2C bus
    bus.close()

if __name__ == "__main__":
    main()
