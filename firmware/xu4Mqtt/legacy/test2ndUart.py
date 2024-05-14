import RPi.GPIO as GPIO
import time

# Constants
BAUD_RATE = 9600  # Baud rate for UART communication
TX_PIN = 15       # GPIO pin for UART transmission
RX_PIN = 14       # GPIO pin for UART reception
BIT_TIME = 1 / BAUD_RATE  # Time for each bit based on baud rate

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TX_PIN, GPIO.OUT)
GPIO.setup(RX_PIN, GPIO.IN)

# Function to receive a bit using the specified GPIO pin
def receive_bit():
    bit = GPIO.input(RX_PIN)
    time.sleep(BIT_TIME)
    return bit

# Function to receive a byte using the RX pin
def receive_byte():
    # Wait for the start bit (0)
    while GPIO.input(RX_PIN) != GPIO.LOW:
        pass
    
    # Align with the bit timing
    time.sleep(BIT_TIME)
    
    # Read each bit of the byte
    byte = 0
    for i in range(8):
        bit = receive_bit()
        byte |= (bit << i)
    
    # Wait for the stop bit (1)
    if GPIO.input(RX_PIN) != GPIO.HIGH:
        print("Error: Stop bit not detected!")
    
    return byte

# Function to read a line from the serial input using the RX pin
def read_line():
    line = []
    while True:
        # Receive a byte using the RX pin
        received_byte = receive_byte()
        received_char = chr(received_byte)
        line.append(received_char)
        
        # Break the loop when a newline character is encountered
        if received_char == '\n':
            break
    
    return ''.join(line)

# Main function
def main():
    print("Starting UART communication using bit banging...")
    
    while True:
        # Read a line using the RX pin
        received_line = read_line()
        
        # Process the received line
        print(f"Received line: {received_line}", end='')

# Cleanup GPIO pins on exit
try:
    main()
finally:
    GPIO.cleanup()
