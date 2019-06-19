#-*- coding: utf-8 -*-
from bluepy.btle import Scanner, DefaultDelegate
from logging import DEBUG
from time import sleep

from bleson import get_provider, Advertiser, Advertisement
import os
import subprocess
import threading
import RPi.GPIO as GPIO

import random

LIGHT_WHITE = 21 #SCANNING
LIGHT_GREEN = 26 #NODE1
LIGHT_YELLOW = 19 #NODE2
LIGHT_RED = 16 #NODE3
LIGHT_BLUE = 20 #NODE4

Content = []
#save devicename for checking devicename(no cycle)
reList = []
#save total device name for readvertising
check=1

def scan():
    print("############### SCANNING START #################")
    scanner = Scanner()
    myThreading = threading.Thread(target=lighting, args=(LIGHT_WHITE,))
    myThreading.start()
    devices = scanner.scan(7.0)
    
    print(" ")
    for dev in devices:
        for (adtype, desc, value) in dev.getScanData():
            if(("ID" in value) or ("R1" in value) or ("R2" in value) or ("R3" in value) or ("R4" in value) or ("R5" in value)):
                if(checkID(value) == 1):
                    return value
    
    return 0

def advertising(name):
    adapter = get_provider().get_adapter()

    advertiser = Advertiser(adapter)
    advertisement = Advertisement()
    
    deviceName = updateName(name)
    #print("CHANGE >> "+deviceName)
    change(deviceName)
    
    advertisement.name = name
    
    advertiser.advertisement = advertisement

    color = deviceName[1]
    
    advertiser.start()
    #print("color >> "+color)
    if(color == "1"):
        lighting(LIGHT_GREEN)
    elif(color == "2"):
        lighting(LIGHT_YELLOW)
    elif(color == "3"):
        lighting(LIGHT_RED)
    elif(color == "4"):
        lighting(LIGHT_BLUE)
    sleep(1)
    advertiser.stop()

def checkID(value):
#chechID >> check devicename 
    check = value[2:6]
    for con in Content:
        if(con == check):
            return 0
    #print("check is " + check)
    Content.append(check[0:4])
    return 1
    

def incFlag(result):#flag 1 increament
    print("RECEIVED SOS SIGNAL : "+result)
    strResult = str(result)
    if("ID" in strResult):
        strResult = strResult.replace("ID","R1")
    elif("R1" in strResult):
        #print("change R2")
        strResult = strResult.replace("R1","R2")
    elif("R2" in strResult):
        strResult = strResult.replace("R2","R3")
    elif("R3" in strResult):
        strResult = strResult.replace("R3","R4")
    elif("R4" in strResult):
        strResult = strResult.replace("R4","R5")
    #print("현재 노드 이름 : "+strResult)
    reList.append(strResult)
    print("################ SCANNING END ##################")
    return strResult

def change(sos):
    cmd = "sudo hciconfig hic0 name " + sos
    return_value = subprocess.call(cmd, shell=True)
    #print('returned value:', return_value)

def lighting(color):
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup( color, GPIO.OUT)
    GPIO.setwarnings(False)
    print("LIGHTING NUM : "+str(color))
    for num in range(1,5):
        GPIO.output(color, True)
        sleep(1)
        GPIO.output(color, False)
        sleep(0.4)
    GPIO.cleanup()

def updateName(name):
    if(len(name)==20):
        return name[0:6] + name[18:20]
    elif(len(name)==21):
        return name[0:6] + name[18:21]
    elif(len(name)==22):
        return name[0:6] + name[18] + "00"
################# MAIN ###################
while(1):
    result = scan()
    if(result == 0):
        check=check+1
        #print("check number >> "+str(check))

    sleep(random.randrange(1,2))

    if(result != 0):
        deviceName1 = incFlag(result)
        #deviceName = updateName(deviceName1)
        #change(deviceName)
        print("############## ADVERTISING START  ##############")
        print("현재 노드 이름 : "+ deviceName1)
        advertising(deviceName1)
        print("############## ADVERTISING END #################")

    if(check%2==0): #readvertising         
        print("############ READVERTISING START ###############")
        for name in reList:
            advertising(name)
            print("readvertising devicename >> "+name)
            advertising(name)

        result = 0
        print("############ READVERTISING END #################")
        
    
    print("=============== Raspberry PI in SOS content lists ===============")
    for contents in Content:
        print(contents)
    print("=================================================================")
    print(" ")
    
    
    if(check>30000):
        check=1
