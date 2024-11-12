import smbus2
import time

# I²C address of the device
address = 0x40

# Initialize I²C bus
bus = smbus2.SMBus(5)  # Use '1' for Raspberry Pi's I²C bus

def read_reg(reg, length):
    """
    Read a specified number of bytes from a given register over I²C.
    """
    try:
        # Write the register address we want to read from
        bus.write_byte(address, reg)
        # Delay to allow sensor time for processing
        time.sleep(0.02)
        # Read the specified number of bytes
        return bus.read_i2c_block_data(address, reg, length)
    except Exception as e:
        print("Error reading register:", e)
        return None

def calculate_temperature_and_humidity(buf):
    """
    Calculate temperature (C) and humidity (%RH) from raw data.
    """
    # Combine bytes into integers
    data = (buf[0] << 8) | buf[1]
    data1 = (buf[2] << 8) | buf[3]

    # Calculate temperature and humidity
    temp = (data * 165.0 / 65535.0) - 40.0
    hum = (data1 / 65535.0) * 100.0

    return temp, hum

def main():
    while True:
        # Read 4 bytes from register 0x00
        buf = read_reg(0x00, 4)
        
        if buf:
            # Calculate temperature and humidity
            temp, hum = calculate_temperature_and_humidity(buf)
            
            # Print results
            print(f"temp(C): {temp:.2f}\thum(%RH): {hum:.2f}")
        else:
            print("Failed to read data")
        
        # Wait for 500 ms before the next reading
        time.sleep(0.5)

# Run the main function
if __name__ == "__main__":
    main()
