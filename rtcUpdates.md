
# Setting Up RTC on Raspberry Pi

This guide covers how to set up NTP (Network Time Protocol) for synchronizing time from internet servers and configure an RTC (Real-Time Clock) on your Raspberry Pi for fallback timekeeping when the internet is unavailable.

## 1. Install NTP (Network Time Protocol)


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















```bash
sudo apt update
sudo apt install ntp
```
By default, NTP will sync time from internet time servers. You can configure custom time servers by editing the NTP configuration file if needed.


Initialize the RTC with the correct time if necessary:
```bash
sudo hwclock -w
```
You can check the time with:
```bash
date # For system time 
sudo hwclock -r # for the RTC time
```
3. Configure Fallback to RTC
Ubuntu should already try to use NTP by default and fall back to the RTC if no internet is available. However, you can automate this by ensuring that the RTC syncs with the system time when the system boots and when no internet is available.

Check Time on Boot: To sync time from the RTC on boot, add the following to```/lib/udev/hwclock-set:```

Find these lines:
```bash
if [ yes = "$BADYEAR" ] ; then
    /sbin/hwclock --rtc=$dev --hctosys --badyear
else
    /sbin/hwclock --rtc=$dev --hctosys
fi

```
Add the command to prevent the system from resetting the RTC time:
```bash
/sbin/hwclock --hctosys
```
Periodically Sync with RTC: Add a cron job to sync with the RTC if NTP fails. Edit the crontab:
```bash
sudo crontab -e
```
Add the following:
```
*/10 * * * * /sbin/hwclock --hctosys >/dev/null 2>&1
```
This will check the RTC every 10 minutes and set the system clock if the internet is unavailable.

4. Verify Everything Works
You can verify that the system uses NTP when internet is available by running:
```
timedatectl status
```
This will show whether the time is synced over NTP or from the RTC.

By using these steps, your Raspberry Pi will automatically synchronize time from the internet when available and fall back to the RTC when it isn't.


1. Install NTP and RTC
Make sure you've already installed NTP and set up your RTC as described in the previous instructions.

2. Sync RTC Time from System Time
When the internet is available, the system time will be updated automatically by NTP. To sync this updated system time to the RTC, you can use the hwclock command.

To set the RTC time based on the current system time:
```
sudo hwclock -w

```
This command writes the system time (which should be accurate after NTP sync) to the RTC.

3. Automate RTC Time Update on Internet Availability
You can automate this process by detecting if the internet is available and then syncing the RTC time. You can add this logic in a script or a cron job that periodically checks for internet connectivity.

Script Example: Sync RTC if Internet is Available
Create a script to check for internet availability and update the RTC if connected:

Create a new script:
```
sudo nano /usr/local/bin/update-rtc.sh
```
Add the following script:
```
#!/bin/bash

# Check for internet connectivity by pinging Google DNS
if ping -c 1 8.8.8.8 &> /dev/null
then
    echo "Internet is available. Syncing system time to RTC..."
    sudo hwclock -w
else
    echo "No internet connection. Skipping RTC sync."
fi

```
Make the script executable:
```
sudo chmod +x /usr/local/bin/update-rtc.sh

```
4. Schedule the Script to Run Periodically
To ensure that the RTC gets updated automatically when the internet is available, you can use a cron job to run the script at regular intervals.

Open the crontab:
```
sudo crontab -e
```
Add a cron job to run the script every 10 minutes (or at your desired interval):
```
*/10 * * * * /usr/local/bin/update-rtc.sh
```
This will check for internet connectivity every 10 minutes and update the RTC if the internet is available.

5. Verify the Setup
After creating the script and cron job, you can test the script manually:
```
sudo /usr/local/bin/update-rtc.sh
```
If the internet is available, the RTC time will be updated from the system time. The cron job will ensure that this happens automatically at regular intervals.

## New Installations from Wearable 
```


```



