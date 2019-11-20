import RPi.GPIO as GPIO    
from time import sleep


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    

GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

lastInput = 0
while True:
    currentInput = GPIO.input(4)
    if(lastInput != currentInput):
        print("A change occured")
        GPIO.output(18, currentInput)
    lastInput = currentInput
