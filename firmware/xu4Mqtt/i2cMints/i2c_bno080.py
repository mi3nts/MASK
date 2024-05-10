import time 

BNO080_I2C_ADDR =  0x4A

SHTP_REPORT_PRODUCT_ID_REQUEST = 0xF9
CHANNEL_CONTROL = 2
DEFAULT_INT_PIN = 255


# Channel numbers
CHANNEL_COMMAND = 0
CHANNEL_EXECUTABLE = 1
CHANNEL_CONTROL = 2
CHANNEL_REPORTS = 3
CHANNEL_WAKE_REPORTS = 4
CHANNEL_GYRO = 5

# SHTP report commands
SHTP_REPORT_COMMAND_RESPONSE = 0xF1
SHTP_REPORT_COMMAND_REQUEST = 0xF2
SHTP_REPORT_FRS_READ_RESPONSE = 0xF3
SHTP_REPORT_FRS_READ_REQUEST = 0xF4
SHTP_REPORT_PRODUCT_ID_RESPONSE = 0xF8
SHTP_REPORT_PRODUCT_ID_REQUEST = 0xF9
SHTP_REPORT_BASE_TIMESTAMP = 0xFB
SHTP_REPORT_SET_FEATURE_COMMAND = 0xFD

# Sensor report IDs
SENSOR_REPORTID_ACCELEROMETER = 0x01
SENSOR_REPORTID_GYROSCOPE = 0x02
SENSOR_REPORTID_MAGNETIC_FIELD = 0x03
SENSOR_REPORTID_LINEAR_ACCELERATION = 0x04
SENSOR_REPORTID_ROTATION_VECTOR = 0x05
SENSOR_REPORTID_GRAVITY = 0x06
SENSOR_REPORTID_UNCALIBRATED_GYRO = 0x07
SENSOR_REPORTID_GAME_ROTATION_VECTOR = 0x08
SENSOR_REPORTID_GEOMAGNETIC_ROTATION_VECTOR = 0x09
SENSOR_REPORTID_GYRO_INTEGRATED_ROTATION_VECTOR = 0x2A
SENSOR_REPORTID_TAP_DETECTOR = 0x10
SENSOR_REPORTID_STEP_COUNTER = 0x11
SENSOR_REPORTID_STABILITY_CLASSIFIER = 0x13
SENSOR_REPORTID_RAW_ACCELEROMETER = 0x14
SENSOR_REPORTID_RAW_GYROSCOPE = 0x15
SENSOR_REPORTID_RAW_MAGNETOMETER = 0x16
SENSOR_REPORTID_PERSONAL_ACTIVITY_CLASSIFIER = 0x1E
SENSOR_REPORTID_AR_VR_STABILIZED_ROTATION_VECTOR = 0x28
SENSOR_REPORTID_AR_VR_STABILIZED_GAME_ROTATION_VECTOR = 0x29

# FRS Record IDs
FRS_RECORDID_ACCELEROMETER = 0xE302
FRS_RECORDID_GYROSCOPE_CALIBRATED = 0xE306
FRS_RECORDID_MAGNETIC_FIELD_CALIBRATED = 0xE309
FRS_RECORDID_ROTATION_VECTOR = 0xE30B

# Executable reset complete
EXECUTABLE_RESET_COMPLETE = 0x1

# Command IDs
COMMAND_ERRORS = 1
COMMAND_COUNTER = 2
COMMAND_TARE = 3
COMMAND_INITIALIZE = 4
COMMAND_DCD = 6
COMMAND_ME_CALIBRATE = 7
COMMAND_DCD_PERIOD_SAVE = 9
COMMAND_OSCILLATOR = 10
COMMAND_CLEAR_DCD = 11

# Calibration
CALIBRATE_ACCEL = 0
CALIBRATE_GYRO = 1
CALIBRATE_MAG = 2
CALIBRATE_PLANAR_ACCEL = 3
CALIBRATE_ACCEL_GYRO_MAG = 4
CALIBRATE_STOP = 5

# Tare commands
TARE_NOW = 0
TARE_PERSIST = 1
TARE_SET_REORIENTATION = 2

# Tare axis
TARE_AXIS_ALL = 0x07
TARE_AXIS_Z = 0x04

# Tare sensor types
TARE_ROTATION_VECTOR = 0
TARE_GAME_ROTATION_VECTOR = 1
TARE_GEOMAGNETIC_ROTATION_VECTOR = 2
TARE_GYRO_INTEGRATED_ROTATION_VECTOR = 3
TARE_AR_VR_STABILIZED_ROTATION_VECTOR = 4
TARE_AR_VR_STABILIZED_GAME_ROTATION_VECTOR = 5

# Packet sizes
MAX_PACKET_SIZE = 128  # Maximum packet size in bytes (packets can be up to 32k, but this value is a reasonable limit)
MAX_METADATA_SIZE = 9  # Maximum metadata size in words (this is in words, often 9 is sufficient)


class BNO080:
    # Assume other class members are defined
    def __init__(self, i2c_device):
        self.device_address =  BNO080_I2C_ADDR
        self.bus = i2c_device
        # self.int_pin = int_pin if int_pin is not None else self.DEFAULT_INT_PIN
        # self.debug = debug
        self.shtp_data = bytearray(14)  # Array to hold received data
        self.sequence_number = [0] * 6  # Initialize sequence numbers for 6 channels

    def initiate(self):
        # Perform a soft reset on the IMU
        # self.soft_reset()
        time.sleep(0.1)  # Add some delay after reset

        # Request product ID and reset info
        self.shtp_data[0] = SHTP_REPORT_PRODUCT_ID_REQUEST
        self.shtp_data[1] = 0

        # Transmit the packet on channel 2, with 2 bytes
        self.send_packet(CHANNEL_CONTROL, 2)

        # Wait for a response
        if self.receive_packet():
            if self.shtp_data[0] == 0xF9:  # SHTP_REPORT_PRODUCT_ID_RESPONSE
                print(f"SW Version Major: 0x{self.shtp_data[2]:02X}")
                print(f"SW Version Minor: 0x{self.shtp_data[3]:02X}")
                sw_part_number = (self.shtp_data[7] << 24) | (self.shtp_data[6] << 16) | \
                                    (self.shtp_data[5] << 8) | self.shtp_data[4]
                print(f"SW Part Number: 0x{sw_part_number:08X}")
                sw_build_number = (self.shtp_data[11] << 24) | (self.shtp_data[10] << 16) | \
                                    (self.shtp_data[9] << 8) | self.shtp_data[8]
                print(f"SW Build Number: 0x{sw_build_number:08X}")
                sw_version_patch = (self.shtp_data[13] << 8) | self.shtp_data[12]
                print(f"SW Version Patch: 0x{sw_version_patch:04X}")
                return True
        return False  # Something went wrong


    def send_packet(self, channel_number, data_length):
        # Calculate the total packet length including header (4 bytes)
        packet_length = data_length + 4
        
        # Create the packet to send
        packet = []
        packet.append(packet_length & 0xFF)  # Packet length LSB
        packet.append(packet_length >> 8)    # Packet length MSB
        packet.append(channel_number)        # Channel number
        packet.append(self.sequence_number[channel_number])  # Sequence number
        # Increment the sequence number for the channel
        self.sequence_number[channel_number] += 1
        
        # Add user's data packet to the list
        packet.extend(self.shtp_data[:data_length])
        
        # Write the packet using SMBus
        try:
            self.bus.write_i2c_block_data(self.device_address, 0, packet)
            return True
        except IOError as e:
            print(f"send_packet(I2C): I/O error: {e}")
            return False
        
    def receive_packet(self):
        # Read the first four bytes to get the packet header
        try:
            header = self.bus.read_i2c_block_data(self.device_address, 0, 4)
        except IOError as e:
            print(f"receive_packet: I/O error: {e}")
            return False
        
        packet_lsb, packet_msb, channel_number, sequence_number = header
        
        # Store the header information
        self.shtp_header[0] = packet_lsb
        self.shtp_header[1] = packet_msb
        self.shtp_header[2] = channel_number
        self.shtp_header[3] = sequence_number

        # Calculate the number of data bytes in this packet
        data_length = ((packet_msb << 8) | packet_lsb) & 0x7FFF  # Clear MSB
        
        if data_length == 0:
            # Packet is empty
            return False  # All done

        # Adjust data length to exclude header
        data_length -= 4
        
        # Read the incoming data into the shtp_data array
        try:
            data = self.bus.read_i2c_block_data(self.device_address, 0, data_length)
            self.shtp_data[:data_length] = data
        except IOError as e:
            print(f"receive_packet: I/O error: {e}")
            return False
        
        # Process packet based on channel number and other conditions
        if channel_number == self.CHANNEL_EXECUTABLE and self.shtp_data[0] == self.EXECUTABLE_RESET_COMPLETE:
            self.has_reset = True

        return True  # Packet received successfully