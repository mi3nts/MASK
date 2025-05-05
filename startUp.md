# startUp

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


## Enabling Wi-Fi, I2C and the serial Port. 

- Use Raspi Config 
```
sudo raspi-config
```

- Check wpa_supplimant file 

```
sudo  nano /etc/wpa_supplicant/wpa_supplicant.cpnf
```

- Reboot the Pi
```sudo reboot```

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
## Library Updates -if needed  
```
  pip3 install adafruit-circuitpython-gps
  pip3 install adafruit-extended-bus
  pip3 install adafruit-circuitpython-icm20x
```
