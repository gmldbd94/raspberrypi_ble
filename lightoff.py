import RPi.GPIO as GPIO

def lightoff():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setwarnings(False)
    
    GPIO.setup(19 , GPIO.OUT)
    GPIO.setup(20 , GPIO.OUT)
    GPIO.setup(21 , GPIO.OUT)
    GPIO.setup(26 , GPIO.OUT)
    GPIO.setup(16 , GPIO.OUT)
    
    GPIO.output(19, False)    
    GPIO.output(20, False)    
    GPIO.output(21, False)    
    GPIO.output(26, False)    
    GPIO.output(16, False)
    GPIO.cleanup()
    
######MAIN####
lightoff()