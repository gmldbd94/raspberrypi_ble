
#-*- coding: utf-8 -*-
from bluepy.btle import Scanner, DefaultDelegate
from logging import DEBUG
from time import sleep

from bleson import get_provider, Advertiser, Advertisement
import os

Content = []
#save MacAddress for checking MacAddress(no cycle)

def scan():
    scanner = Scanner()
    devices = scanner.scan(10.0)
    result=" "

    for dev in devices:
        for (adtype, desc, value) in dev.getScanData():
            if(("ID" in value) or ("R1" in value) or ("R2" in value) or ("R3" in value) or ("R4" in value) or ("R5" in value)):
                if(checkID(value) == 1):
                    return value
    return 0

def advertising(deviceName):
    adapter = get_provider().get_adapter()

    advertiser = Advertiser(adapter)
    advertisement = Advertisement()
    advertisement.name = deviceName

    advertiser.advertisement = advertisement

    advertiser.start()
    sleep(10)
    advertiser.stop()


def checkID(value):
#chechID >> check MacAddress 
    check = value[2:]
    for con in Content:
        if(con == check):
            return 0
    
    Content.append(check)
    return 1
    

def incFlag(result):
#flag 1 increament
    strResult = str(result)
    if("ID" in strResult):
        strResult = strResult.replace("ID","R1")
    elif("R1" in strResult):
        strResult = strResult.replace("R1","R2")
    elif("R2" in strResult):
        strResult = strResult.replace("R2","R3")
    elif("R3" in strResult):
        strResult = strResult.replace("R3","R4")
    elif("R4" in strResult):
        strResult = strResult.replace("R4","R5")

    return strResult

result = scan()

if(result != 0):
    deviceName = incFlag(result)
    print(deviceName + "re")
    os.system('sudo hciconfig hic0 name '+ deviceName)
    advertising(deviceName)

print(deviceName)
