# MASK
Mints Automobile Sensing Kit 

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


## SD Card Installation 
Download Rasberry Pi Imager to your PC via this [link](https://www.raspberrypi.com/software/).


## Install DW Service 
```
wget https://dwservice.net/download/dwagent.sh
chmod +x dwagent.sh 
sudo ./dwagent.sh 
```
Follow the on screen instructions 


## Install Pi Zero SW 
```
curl http://cdn.pisugar.com/release/pisugar-power-manager.sh | sudo bash
```
After the installation finishes - Go to the http://<your raspberry ip>:8421 page and update the RTC Clock on the PI Sugar 3 

![link](https://raw.githubusercontent.com/mi3nts/minWeZeroRPiOS/main/res/piSugar3.png)

## For the IPS7100 to work on the GPIO Serial Port
To manually change the settings, edit the kernel command line with `sudo nano /boot/cmdline.txt`. Find the console entry that refers to the serial0 device, and remove it, including the baud rate setting. It will look something like `console=serial0,115200`. Make sure the rest of the line remains the same, as errors in this configuration can stop the Raspberry Pi from booting.

## New Image on the pi
- Add dwservice tag
- Start the rasberry pi via main power 
- update both the rtc as well as the pi time via the pisugar interface



## Basic Installation Steps
- Using the rasberry pi imager do an sd card image


- Using Raspi Config, enable Wi-Fi, I2C and the serial Port. 
```
sudo raspi-config
```

- Check wpa_supplimant file 
```
sudo  nano /etc/wpa_supplicant/wpa_supplicant.cpnf
```
- Reboot the Pi
```sudo reboot```

- Install dwservice 
```
https://www.dwservice.net/download/dwagent.sh
chmod +x dwagent.sh 
sudo ./dwagent.sh 
```
- clone the git repo 
```
mkdir gitHubRepos
```

- Install pisugaru SW
```
curl http://cdn.pisugar.com/release/pisugar-power-manager.sh | sudo bash
```
 - Update pisugar SW
```
curl https://cdn.pisugar.com/release/PiSugarUpdate.sh | sudo bash
```
- Add an extra I2c Pipeline 
On the to /boot/config.txt add the following lines `dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24` And connect the secondary I2C devices to gpio pins 23(16) and 24(18).
 ```
 sudo nano /boot/config.txt
 ```


- Update pi sugar
``` curl https://cdn.pisugar.com/release/PiSugarUpdate.sh | sudo bash```

 ## OTA updates 
``` curl https://cdn.pisugar.com/release/PiSugarUpdate.sh | sudo bash```

## GPS Updates 
```
  pip3 install adafruit-circuitpython-gps
  pip3 install adafruit-extended-bus
```

## Data Sheet links 
* [BME280: 1](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf)
* [BME280: 2](https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/downloads)

**Note:GPIO pins are not header numbers**

The pin diagrams for the rasbery pi zero are given below:
<img src="https://raw.githubusercontent.com/mi3nts/minWeZeroNodes/main/res/Raspberry-PI-Zero-Pinout-schema.jpg.webp"
     alt="Rasberry Pi Zero Pin Outs"
     style="float: left; margin-right: 10px;" />


