
#-*- coding: utf-8 -*-
from bluepy.btle import Scanner, DefaultDelegate
from logging import DEBUG
from time import sleep

from bleson import get_provider, Advertiser, Advertisement
import os
import subprocess
import threading
import RPi.GPIO as GPIO

Content = []
#save MacAddress for checking MacAddress(no cycle)

def scan():
    print("scanning")
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
    print("advertising")
    adapter = get_provider().get_adapter()

    advertiser = Advertiser(adapter)
    advertisement = Advertisement()
    advertisement.name = deviceName

    advertiser.advertisement = advertisement

    advertiser.start()
    sleep(15)
    advertiser.stop()
    sleep(0.5)

def checkID(value):
#chechID >> check MacAddress 
    check = value[2:7]
    for con in Content:
        if(con == check):
            return 0
    print("check is " + check)
    Content.append(check[0:5])
    return 1
    

def incFlag(result):
#flag 1 increament
    print("start incFlag")
    strResult = str(result)
    if("ID" in strResult):
        strResult = strResult.replace("ID","R1")
    elif("R1" in strResult):
        print("change R2")
        strResult = strResult.replace("R1","R2")
    elif("R2" in strResult):
        strResult = strResult.replace("R2","R3")
    elif("R3" in strResult):
        strResult = strResult.replace("R3","R4")
    elif("R4" in strResult):
        strResult = strResult.replace("R4","R5")
    print(strResult)
    return strResult

def change(sos):
    cmd = "sudo hciconfig hic0 name " + sos
    return_value = subprocess.call(cmd, shell=True)
    print('returned value:', return_value)

def lighting():
    GPIO.setmode(GPIO.BOARD)
    print("123123")
    
    GPIO.setup( 12, GPIO.OUT)
    for num in range(1,10):
        print("redDDDDDDDDDDDDDDDDDDDDDDDD")
        GPIO.output(12, GPIO.HIGH)
        sleep(1)
        GPIO.output(12, GPIO.LOW)
        sleep(1)
    GPIO.cleanup()

################# MAIN ###############    
while(1):
    result = scan()

    if(result != 0):
        myThreading = threading.Thread(target=lighting, args=())
        myThreading.start()
        deviceName = incFlag(result)
        deviceName = deviceName[0:7]
        change(deviceName)
        advertising(deviceName)
        os.system('ps')
    print("현재 노드 이름:"+deviceName)
    print("##########Raspberry PI in SOS content lists##############")
    for contents in Content:
        print(contents)
