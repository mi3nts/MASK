#!/bin/bash
#
sleep 60
kill $(pgrep -f 'ipsI2CReader.py')
sleep 5
python3 ipsI2CReader.py &
sleep 5

kill $(pgrep -f 'climateReader.py')
sleep 5
python3 climateReader.py &
sleep 5

kill $(pgrep -f 'bno080Reader.py')
sleep 5
python3 bno080Reader.py &
sleep 5

kill $(pgrep -f 'cozIRReader.py')
sleep 5
python3 cozIRReader.py &
sleep 5

kill $(pgrep -f 'gpsReader.py')
sleep 5
python3 gpsReader.py &
sleep 5

kill $(pgrep -f 'batteryReader.py')
sleep 5
python3 batteryReader.py &
sleep 5


python3 ipReader.py
sleep 5