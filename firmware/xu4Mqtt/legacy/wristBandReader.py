# from network import Bluetooth

# bluetooth = Bluetooth()
# bluetooth.start_scan(-1)    # start scanning with no timeout

# while True:
#     print(bluetooth.get_adv())
import struct

import time
from collections import OrderedDict
# Protocol defined here:
#     https://github.com/zh2x/BCI_Protocol
# Thanks as well to:
#     https://github.com/ehborisov/BerryMed-Pulse-Oximeter-tool
#     https://github.com/ScheindorfHyenetics/berrymedBluetoothOxymeter
#
# The sensor updates the readings at 100Hz.
import datetime
import _bleio
import adafruit_ble
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble.services.nordic import UARTService 
uart = UARTService()
uart_connection = None
from mintsXU4 import mintsSensorReader as mSR

# from adafruit_ble_berrymed_pulse_oximeter import BerryMedPulseOximeterService

# CircuitPython <6 uses its own ConnectionError type. So, is it if available. Otherwise,
# the built in ConnectionError is used.
connection_error = ConnectionError
if hasattr(_bleio, "ConnectionError"):
    connection_error = _bleio.ConnectionError

# PyLint can't find BLERadio for some reason so special case it here.
ble = adafruit_ble.BLERadio()  # pylint: disable=no-member

wrist_band_connection = None

while True:
    print("Scanning...")
    for adv in ble.start_scan(Advertisement, timeout=5):
        name = adv.complete_name
        print(adv)
        print(name)
        if not name:
            continue
        if name.strip("\x00") == "MINTSWearable001":
            wrist_band_connection = ble.connect(adv)
            print(wrist_band_connection)
            print("Connected")
            break
    # Stop scanning whether or not we are connected.
    ble.stop_scan()
    print("Stopped scan")
    # time.sleep(5)
    # print(wrist_band_connection)
    # print(wrist_band_connection.connected)
    # time.sleep(5)
    try:
        if wrist_band_connection and wrist_band_connection.connected:
            print("Fetch connection")
            print(wrist_band_connection)
            uart_service = wrist_band_connection[UARTService]
            while wrist_band_connection.connected:    
                byteArrayReceived = uart_service.read(4)
                if byteArrayReceived:
                    dateTime = datetime.datetime.now()
                    sensorIDIndex    = struct.unpack('<B',bytes.fromhex(\
                                            byteArrayReceived.hex()[0:2]))[0]
                    parametorIDIndex = struct.unpack('<B',bytes.fromhex(\
                                            byteArrayReceived.hex()[2:4]))[0]
                    if sensorIDIndex == 61: 
                        if parametorIDIndex  == 1:
                            hrAmplitude =  struct.unpack('<H',bytes.fromhex(\
                                            byteArrayReceived.hex()[4:8]))[0]
                            sensorDictionary =  OrderedDict([
                                    ("dateTime"    ,str(dateTime)),
                                    ("hrAmplitude" ,str(hrAmplitude))
                            ])
                            print(sensorDictionary)
                            mSR.sensorFinisher(dateTime,"PSA109",sensorDictionary)
                    
                    if sensorIDIndex == 27: 
                        if parametorIDIndex  == 1:
                            if byteArrayReceived.hex()[4:8]!= "ffff":
                                hexArray    = byteArrayReceived.hex()
                                hexArray    = hexArray[:6] + "0" + hexArray[6 + 1:]
                                int32HexStr  = "0000" + hexArray[6:8]+ hexArray[4:6]
                                int32In  = struct.unpack('>I',bytes.fromhex(\
                                            int32HexStr))[0]
                                temperature = int32In/16.0
                                int1 = int.from_bytes(bytearray.fromhex(int32HexStr), byteorder='big')
                                int2 = int.from_bytes(bytearray([0,1,0,0]) , byteorder='big')
                                if int1  & int2:
                                     temperature = temperature-256
                                sensorDictionary =  OrderedDict([
                                    ("dateTime"    ,str(dateTime)),
                                    ("temperature" ,str(temperature))
                                ])
                                print(sensorDictionary)
                                mSR.sensorFinisher(dateTime,"MCP9808",sensorDictionary)
    except connection_error:
        try:
            pulse_ox_connection.disconnect()
        except connection_error:
            pass
        pulse_ox_connection = None
