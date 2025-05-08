
# Setting Up RTC on Raspberry Pi

This guide covers how to set up NTP (Network Time Protocol) for synchronizing time from internet servers and configure an RTC (Real-Time Clock) on your Raspberry Pi for fallback timekeeping when the internet is unavailable.


## Start by updating the piSugar SW Stack 

```bash 
curl https://cdn.pisugar.com/release/PiSugarUpdate.sh | sudo bash
```

## Install NTP (Network Time Protocol)

First, install NTP to synchronize time from a time server:

1. Install and Configure the RTC
If you haven't already set up an RTC on your Raspberry Pi, follow these steps:

Install I2C tools if needed:
```bash
sudo apt-get install i2c-tools
```
Check if the RTC is detected on the I²C bus:
```bash
sudo i2cdetect -y 1
```
Add the RTC module to the system:

Add the following to /boot/config.txt
```bash
dtparam=i2c_arm=on
dtoverlay=i2c-rtc,ds3231
```
Replace ds3231 with your RTC model if needed
Reboot:
```bash
sudo reboot
```

2. Remove Unenecessary Clocks and Syncs 

Remove fake-hwclock, which can interfere with your RTC:
```bash
sudo apt-get remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
```
Remove ntp 

```bash 
sudo apt remove --purge ntp
```

3.  Install systemd-timesyncd
```bash
sudo apt update
sudo apt install systemd-timesyncd
```

4. Enable systemd-timesyncd
```bash
sudo systemctl enable systemd-timesyncd
sudo systemctl start systemd-timesyncd
sudo timedatectl set-ntp true
```
5. Check
```bash 
timedatectl status
```
This should return 
```bash 
System clock synchronized: yes
NTP service: active
```

6. Comment /lib/udev/hwclock-set


``` bash 
#!/bin/sh
# Reset the System Clock to UTC if the hardware clock from which it
# was copied by the kernel was in localtime.

#dev=$1

#if [ yes = "$BADYEAR" ] ; then
#    /sbin/hwclock --rtc=$dev --hctosys --badyear
#else
#    /sbin/hwclock --rtc=$dev --hctosys
#fi


#if [ -e /run/systemd/system ] ; then
#    exit 0
#fi
```

6. Final set up for the clock 
``` bash 
git clone git@github.com:mi3nts/MASK.git
sudo cp firmware/xu4Mqtt/sudoRun.sh /usr/local/bin/update-rtc.sh
```
Add the line `/usr/local/bin/update-rtc.sh` to `/etc/rc.local`  before exit 0
```
sudo nano /etc/rc.local
```

```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

/usr/local/bin/update-rtc.sh

exit 0
```
