#!/bin/bash
#
sleep 6
kill $(pgrep -f 'ips7100Reader.py')
sleep 5
python3 ips7100Reader.py &
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