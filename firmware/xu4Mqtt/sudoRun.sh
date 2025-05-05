#!/bin/bash

# ================================
# Raspberry Pi Zero - Time Sync Script
# Using timedatectl + systemd-timesyncd + RTC
# ================================

sleep 10

LOG_FILE="/var/log/time_sync.log"

# Function to log messages to console + log file
log_message() {
    echo "$(date): $1" | tee -a "$LOG_FILE"
}

echo "Starting time synchronization process..."

# (Optional) First boot setup
if [ -f /aafirstboot ]; then 
    echo "First boot setup detected. Running /aafirstboot start..."
    /aafirstboot start
fi

# Check for internet connection
if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    echo "Internet connection detected. Attempting NTP synchronization..."
    log_message "Internet detected. Enabling NTP sync with timedatectl..."
    
    # Ensure NTP syncing is enabled
    sudo timedatectl set-ntp true

    # Restart systemd-timesyncd to force immediate sync
    sudo systemctl restart systemd-timesyncd

    # Wait a bit for sync to happen
    sleep 10

    # Check if NTP synchronization happened
    if timedatectl show | grep -q "NTPSynchronized=yes"; then
        echo "NTP synchronized successfully. Writing system time to RTC..."
        log_message "NTP synchronized. Writing system time to RTC..."
        sudo hwclock -w
        echo "System time successfully written to RTC."
        log_message "System time successfully written to RTC."
    else
        echo "NTP synchronization not achieved. Skipping RTC update."
        log_message "NTP NOT synchronized yet. Skipping RTC update."
    fi
else
    echo "No internet connection detected. Loading system time from RTC..."
    log_message "No internet connection detected. Loading system time from RTC..."
    
    # Attempt to load RTC into system clock
    if sudo hwclock -s; then
        echo "System time successfully loaded from RTC."
        log_message "System time successfully loaded from RTC."
    else
        echo "Failed to load system time from RTC!"
        log_message "Failed to load system time from RTC!"
    fi
fi

echo "Time synchronization process complete."
log_message "Time synchronization process complete."

exit 0
