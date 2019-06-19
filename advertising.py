from bleson import get_provider, Advertiser, Advertisement
import os
import sys
import subprocess
from time import sleep
import threading
import RPi.GPIO as GPIO

def advertising(deviceName):
    adapter = get_provider().get_adapter()

    advertiser = Advertiser(adapter)
    advertisement = Advertisement()
    advertisement.name = deviceName
    
    advertiser.advertisement = advertisement

    advertiser.start()
    sleep(5)
    advertiser.stop()
    
def createDeviceName(num):
    return "ID" + str(num) +"3672"

def numLength(parameter):
    num=str(parameter)
    if(len(num)==4):
        return num
    elif(len(num)==3):
        return "0"+num
    elif(len(num)==2):
        return "00"+num
    elif(len(num)==1):
        return "000"+num
    else:
        return "0000"

def change(sos):
    cmd = "sudo hciconfig hic0 name " + sos
    return_value = subprocess.call(cmd, shell=True)
    
def lighton():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setwarnings(False)
    
    GPIO.setup(19 , GPIO.OUT)
    GPIO.setup(20 , GPIO.OUT)
    GPIO.setup(21 , GPIO.OUT)
    GPIO.setup(26 , GPIO.OUT)
    GPIO.setup(16 , GPIO.OUT)
    
    GPIO.output(19, True)    
    GPIO.output(20, True)    
    GPIO.output(21, True)    
    GPIO.output(26, True)    
    GPIO.output(16, True)
    sleep(4.8)
    GPIO.output(19, False)    
    GPIO.output(20, False)    
    GPIO.output(21, False)    
    GPIO.output(26, False)    
    GPIO.output(16, False)
    sleep(0.2)
    GPIO.cleanup()
    

###MAIN###
def main(argv):
    parameter=argv[1]
    num=numLength(parameter)
    deviceName=createDeviceName(num)
    change(deviceName)
    print(deviceName)
    while(1):
        advertising(deviceName)
        lighton()
    
    
if __name__=="__main__":
    main(sys.argv)
