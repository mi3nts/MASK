#!/bin/bash
#
sleep 1
kill $(pgrep -f 'ips7100Reader.py')
sleep 1

kill $(pgrep -f 'climateReader.py')
sleep 1

kill $(pgrep -f 'bno080ReaderV2.py')
sleep 1

kill $(pgrep -f 'cozIRReader.py')
sleep 1

kill $(pgrep -f 'gpsReader.py')
sleep 1

kill $(pgrep -f 'batteryReader.py')
sleep 1
