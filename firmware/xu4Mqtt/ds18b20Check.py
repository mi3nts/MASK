import smbus
import time

# I2C address of the CHT8305C
CHT8305C_ADDRESS = 0x40  # Default I2C address for the sensor

# Register addresses
RESET_REGISTER = 0x02  # Hypothetical reset register (check the datasheet for exact register)
TEMP_HUMIDITY_REGISTER = 0x00  # Assuming the data starts at 0x00

# SMBus setup
bus = smbus.SMBus(5)  # Use 1 for Raspberry Pi or similar systems

def reset_sensor():
    """
    Reset the CHT8305C sensor.
    """
    try:
        print("Resetting sensor...")
        bus.write_byte(CHT8305C_ADDRESS, RESET_REGISTER)
        time.sleep(0.1)  # Allow some time for the sensor to reset
        print("Sensor reset complete.")
    except Exception as e:
        print(f"Error resetting sensor: {e}")

def read_temperature_and_humidity():
    """
    Read temperature and humidity from the CHT8305C sensor.
    Returns:
        tuple: (temperature, humidity)
    """
    try:
        # Read 4 bytes of data from the temperature/humidity register
        data = bus.read_i2c_block_data(CHT8305C_ADDRESS, TEMP_HUMIDITY_REGISTER, 4)
        
        # Process temperature (first two bytes)
        raw_temp = (data[0] << 8) | data[1]
        temperature = -45 + (175 * raw_temp / 65536.0)  # Adjust based on datasheet formula
        
        # Process humidity (next two bytes)
        raw_humidity = (data[2] << 8) | data[3]
        humidity = 100 * raw_humidity / 65536.0  # Adjust based on datasheet formula
        
        return temperature, humidity
    except Exception as e:
        print(f"Error reading data: {e}")
        return None, None

def main():
    """
    Main function to interact with the CHT8305C sensor.
    """
    # Reset the sensor before reading data
    reset_sensor()
    
    # Give the sensor time to initialize after reset
    time.sleep(0.5)
    
    # Read and display temperature and humidity
    temperature, humidity = read_temperature_and_humidity()
    if temperature is not None and humidity is not None:
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
    else:
        print("Failed to read data from sensor.")

if __name__ == "__main__":
    main()
