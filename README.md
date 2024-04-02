# MASK
Mints Automobile Sensing Kit 

# Devices Attached
- Rasberry Pi 2WH
- Pi Sugar 3 Power Manage
- Toggle Switch
- Sensors
  - IPS7100  : I2c or Uart
  - BME280   : I2c (0x77) 
  - COZIR AH : Uart Only 
  - BNO085   : I2c and Uart 
  - PA1010D  : I2c and Uart 
  - BME280   : I2c  
  - TMP117   : I2c

- Since multiple uarts are needed, soft uart can be used: https://github.com/adrianomarto/soft_uart
- Add an extra I2c Pipeline On the to /boot/config.txt add the following lines dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24 And connect the secondary I2C devices to gpio pins 23(16) and 24(18).
