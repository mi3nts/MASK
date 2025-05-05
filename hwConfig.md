# Devices Attached
- Rasberry Pi 2WH
- Pi Sugar 3 Power Manage
- Toggle Switch
- Sensors
  - COZIR AH          : Uart Only           : UART (default)
  - PiSugar and Clock : I2c                 : I2c Bus 1 (default)
  - IPS7100           : I2c or Uart         : I2c Bus 3
    - `dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=27,i2c_gpio_scl=22` Connecting the secondary I2C devices to gpio pins 27(13) and 22(15).
  - BNO085            : I2c, SPI and Uart   : I2c Bus 4
    - `dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24` Connecting the tertiary I2C devices to gpio pins 23(16) and 24(18).
  - BME280            : I2c                 : I2c Bus 5
  - TMP117            : I2c                 : I2c Bus 5
    - `dtoverlay=i2c-gpio,bus=5,i2c_gpio_delay_us=1,i2c_gpio_sda=05,i2c_gpio_scl=06` Connecting the tertiary I2C devices to gpio pins 05(29) and 06(31).
  - PA1010D           : I2c, SPI and Uart   : I2c Bus 6
    - `dtoverlay=i2c-gpio,bus=6,i2c_gpio_delay_us=1,i2c_gpio_sda=25,i2c_gpio_scl=26` Connecting  the secondary I2C devices to gpio pins 25(22) and 26(37).

- Add an extra I2c Pipeline On the to /boot/config.txt add the following lines via ```sudo nano /boot/config.txt```.

```
dtoverlay=i2c-rtc,ds3231
# Extra i2c port 
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=27,i2c_gpio_scl=22
dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24
dtoverlay=i2c-gpio,bus=5,i2c_gpio_delay_us=1,i2c_gpio_sda=05,i2c_gpio_scl=06
dtoverlay=i2c-gpio,bus=6,i2c_gpio_delay_us=1,i2c_gpio_sda=25,i2c_gpio_scl=26
```

- Check Devices<br>
  ```sudo i2cdetect -y 1```<br>
  ```sudo i2cdetect -y 2```<br>
  ```sudo i2cdetect -y 3```<br>
  ```sudo i2cdetect -y 4```<br>
  ```sudo i2cdetect -y 5```<br>

Inspired by this [link](https://www.instructables.com/Raspberry-PI-Multiple-I2c-Devices/) 


<!-- ## For the IPS7100 to work on the GPIO Serial Port
To manually change the settings, edit the kernel command line with `sudo nano /boot/cmdline.txt`. Find the console entry that refers to the serial0 device, and remove it, including the baud rate setting. It will look something like `console=serial0,115200`. Make sure the rest of the line remains the same, as errors in this configuration can stop the Raspberry Pi from booting. -->