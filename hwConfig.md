
# Devices Attached

- **Raspberry Pi 2WH**
- **PiSugar 3 Power Manager**
- **Toggle Switch**
- **Sensors**
  - **COZIR AH**: UART only — connected via **UART** (default)
  - **PiSugar and Clock**: I²C — connected to **I²C Bus 1** (default)
  - **IPS7100**: I²C or UART — connected to **I²C Bus 3**
    - Enable via:
      ```
      dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=27,i2c_gpio_scl=22
      ```
      (GPIO 27 (pin 13) and GPIO 22 (pin 15))
  - **ICM20948**: I²C, SPI, or UART — connected to **I²C Bus 4**
    - Enable via:
      ```
      dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24
      ```
      (GPIO 23 (pin 16) and GPIO 24 (pin 18))
  - **BME280**: I²C — connected to **I²C Bus 5**
  - **TMP117**: I²C — connected to **I²C Bus 5**
    - Enable via:
      ```
      dtoverlay=i2c-gpio,bus=5,i2c_gpio_delay_us=1,i2c_gpio_sda=5,i2c_gpio_scl=6
      ```
      (GPIO 5 (pin 29) and GPIO 6 (pin 31))
  - **PA1010D**: I²C, SPI, or UART — connected to **I²C Bus 6**
    - Enable via:
      ```
      dtoverlay=i2c-gpio,bus=6,i2c_gpio_delay_us=1,i2c_gpio_sda=25,i2c_gpio_scl=26
      ```
      (GPIO 25 (pin 22) and GPIO 26 (pin 37))

---

## Adding Extra I²C Pipelines

To configure additional I²C buses, edit `/boot/config.txt` using:

```bash
sudo nano /boot/config.txt
```

Add the following lines:

```
dtoverlay=i2c-rtc,ds3231
# Extra I2C ports
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=27,i2c_gpio_scl=22
dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24
dtoverlay=i2c-gpio,bus=5,i2c_gpio_delay_us=1,i2c_gpio_sda=5,i2c_gpio_scl=6
dtoverlay=i2c-gpio,bus=6,i2c_gpio_delay_us=1,i2c_gpio_sda=25,i2c_gpio_scl=26
```

Be sure to also check the [config.txt](config) file for additional setup details.

---

## Checking Attached Devices

Use the following commands to detect devices on each I²C bus:

```bash
sudo i2cdetect -y 1
sudo i2cdetect -y 2
sudo i2cdetect -y 3
sudo i2cdetect -y 4
sudo i2cdetect -y 5
```

---

> *Configuration inspired by this [Instructables guide](https://www.instructables.com/Raspberry-PI-Multiple-I2c-Devices/).*

<!-- 
## Notes for IPS7100 UART Setup
To manually reconfigure the GPIO serial port:
- Edit `/boot/cmdline.txt` using:
  ```bash
  sudo nano /boot/cmdline.txt
  ```
- Remove any `console=serial0,115200` entry carefully.
- Do not alter the rest of the line to avoid boot issues.
-->
