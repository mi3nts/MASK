# Battery reader written for Pi Sugar 3 module
# https://github.com/PiSugar/PiSugar/wiki/PiSugar-Power-Manager-(Software)

import datetime
from subprocess import run
import time
from collections import OrderedDict
from mintsXU4 import mintsSensorReader as mSR
import os


loopInterval = 30

debug  = False 

def getPiSugarOutput(command,ignoreStr):
    data = run("echo " +command + " | nc -q 1 127.0.0.1 8423",capture_output=True,shell=True)
    outValue = data.stdout.decode().replace("\n","").replace(ignoreStr,"").replace("true","1").replace("false","0")
    errCode  = data.stderr
    return outValue, errCode;

def main(loopInterval):
    
    startTime    = time.time()
    while True:
        try:
            print("============================================================")
            dateTime          = datetime.datetime.now()
            rtcTime,rtcErr =\
                             getPiSugarOutput("get rtc_time","rtc_time: ")
            batteryPercentage,batteryPercentageErr =\
                             getPiSugarOutput("get battery","battery: ")
            batteryVoltage,batteryVoltageErr =\
                             getPiSugarOutput("get battery_v","battery_v: ")            
            batteryChargingState,batteryChargingErr =\
                             getPiSugarOutput("get battery_charging","battery_charging: ")               
            batteryLedAmount,batteryChargingErr =\
                             getPiSugarOutput("get battery_led_amount","battery_led_amount: ")                         
            batteryPowerPlugged,batteryChargingErr =\
                             getPiSugarOutput("get battery_power_plugged","battery_power_plugged: ")      
            sensorDictionary =  OrderedDict([
                        ("dateTime"               ,str(dateTime)), # always the same
                        ("rtcTime"                ,str(rtcTime)),                     
                        ("batteryPercentage"      ,str(batteryPercentage)),
                        ("batteryVoltage"         ,str(batteryVoltage)), 
                        ("batteryChargingState"   ,str(batteryChargingState)),
                        ("batteryLedAmount"       ,str(batteryLedAmount)), 
                        ("batteryPowerPlugged"    ,str(batteryPowerPlugged)),
                        ])
            print(sensorDictionary)
            if (batteryChargingState == '0' or batteryChargingState == '1'):
                mSR.sensorFinisher(dateTime,"MWBR001",sensorDictionary)
                startTime = mSR.delayMints(time.time() - startTime,loopInterval)
            else:
                print("Invalid Data")
                time.sleep(10)

        except Exception as e:
            print(e)
            break

if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring Battery level for Mints Wearable Node")
    main(loopInterval)
