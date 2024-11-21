#!/bin/bash

sleep 5

kill $(pgrep -f 'bno080WithPa1010dReader.py')
sleep 1

kill $(pgrep -f 'ips7100Reader.py')
sleep 1

kill $(pgrep -f 'bme280WithCht8305cReader.py')
sleep 1

kill $(pgrep -f 'cozIRReader.py')
sleep 1

kill $(pgrep -f 'piSugarReader.py')
sleep 1

