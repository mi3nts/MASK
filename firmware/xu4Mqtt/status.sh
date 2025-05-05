#!/bin/bash
#
sleep 1
echo "ICM2094 With PA1010D"
echo $(pgrep -f 'icm20948WithPa1010dReader.py')
sleep 2

echo "IPS7100"
echo $(pgrep -f 'ips7100Reader.py')
sleep 2

echo "GPS"
echo $(pgrep -f 'gpsReader.py')
sleep 2


echo "BME280 With CHT8305C"
echo $(pgrep -f 'bme280WithCht8305cReader.py')
sleep 2

echo "COZIR"
echo $(pgrep -f 'cozIRReader.py')
sleep 2

echo "PI SUGAR"
echo $(pgrep -f 'piSugarReader.py')
sleep 2

echo "IP"
echo $(pgrep -f 'ipReader.py')
sleep 2
