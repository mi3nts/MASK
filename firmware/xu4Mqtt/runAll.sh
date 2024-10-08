#!/bin/bash

sleep 60

kill $(pgrep -f 'bno080WithPa1010dReader.py')
sleep 5
python3 bno080WithPa1010dReader.py &
sleep 5

kill $(pgrep -f 'ips7100Reader.py')
sleep 5
python3 ips7100Reader.py &
sleep 5

kill $(pgrep -f 'bme280WithTmp117Reader.py')
sleep 5
python3 bme280WithTmp117Reader.py &
sleep 5

kill $(pgrep -f 'cozIRReader.py')
sleep 5
python3 cozIRReader.py &
sleep 5

kill $(pgrep -f 'batteryReader.py')
sleep 5
python3 batteryReader.py &
sleep 5

python3 ipReader.py
sleep 5