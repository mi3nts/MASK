import smbus2
import time

# I²C address of the SEN0546 sensor
ADDRESS = 0x40

# Register addresses for the sensor (Refer to the datasheet or sensor's documentation)
TEMP_REG = 0x00  # Example register for temperature (check datasheet)
HUM_REG = 0x01   # Example register for humidity (check datasheet)

# Initialize the I2C bus
bus = smbus2.SMBus(5)  # I2C bus 1 is commonly used on the Raspberry Pi

def read_sensor_data():
    try:
        # Read temperature data from the sensor (2 bytes)
        temp_data = bus.read_i2c_block_data(ADDRESS, TEMP_REG, 2)
        
        # Read humidity data from the sensor (2 bytes)
        hum_data = bus.read_i2c_block_data(ADDRESS, HUM_REG, 2)
        
        # Convert the raw data to meaningful values (temperature and humidity)
        temperature = (temp_data[0] << 8 | temp_data[1]) / 10.0  # Adjust according to the sensor's scale
        humidity = (hum_data[0] << 8 | hum_data[1]) / 10.0     # Adjust according to the sensor's scale
        
        print(f"Temperature: {temperature} °C")
        print(f"Humidity: {humidity} %")

    except Exception as e:
        print(f"Error reading from sensor: {e}")

# Continuously read sensor data every 2 seconds
while True:
    read_sensor_data()
    time.sleep(2)