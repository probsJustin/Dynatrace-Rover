import os
import re
from time import sleep
import serial
from goprocam import GoProCamera
from goprocam import constants
import RPi.GPIO as GPIO  


#DEBUG VARIABLES 

#timeCycle if enabled it will cycle through the time cycle loop for testing instead of doing anything at all

timeCycle = False

#controlLightTest
controlLight = True

#when set to true it will not upload the picture to twitter but will leave it on the raspberry pi as image.png
dryRun = False

#if enabled it will allow for the gopro to take the picture and move it to image.png but this is still dependant on the dry run variable
takePhoto = False

#if true this will use the remote as the trigger - if false it will allow for commands to be ran for debug
allowRemote = True

#turn on lights if true
lights = False



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    

GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)

blue = 18
green = 23
red  = 24

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
counter = 32 # Below 32 everything in ASCII is gibberish

def writeToArduino(text):
    global ser
    returnObject = ""
    ser.write(bytes(text,'utf-8')) # Convert the decimal number to ASCII then send it to the Arduino
    return returnObject 

def readFromArduino():
    global ser
    returnObject = bytes("",'utf-8')
    for x in range(0,3):
        counter = 32 # Below 32 everything in ASCII is gibberish
        returnObject = returnObject + ser.readline() # Read the newest output from the Arduino
        sleep(.2) # Delay for one tenth of a second
        if counter == 255:
            counter = 32
        
    return returnObject

def takePicture():
    gpCam = GoProCamera.GoPro()
    TIMER= 2
    gpCam.downloadLastMedia(gpCam.take_photo(TIMER)) #take a photo in 4 seconds and download it.
    print("Picture has been taken and downloaded.")

def logThis(text):
    print("[LOG]" + text)
    
def movePicture():
    stream = os.popen('ls -l')
    output = stream.read()
    for x in output.splitlines():
        if(x.find('.JPG') > -1):
            print(re.search(r'\d\d\:\d\d\s(.*[.JPG])', x).group(1))
            newstream = os.popen("cp ./" + re.search(r'\d\d\:\d\d\s(.*[.JPG])', x).group(1) + " ./image.png")
            logThis("Copy the picture over to ./image.png")
            newstream = os.popen("rm -f ./" + re.search(r'\d\d\:\d\d\s(.*[.JPG])', x).group(1))
            logThis("Remove the older picture") 
            if(dryRun != True):
                newstream = os.popen("node post")
                print(newstream.read())
                #newstream = os.popen("rm -f ./image.png")
            else:
                logThis("***Dry Run ***")
            logThis("Picture Sent To Twitter")
            
if(takePhoto):
    logThis("Picture Will Be Taken")
    takePicture()
    logThis("Picture Taken")
    movePicture()
else:
    logThis("Picture Will Not Be Taken")


if(timeCycle):
    while True:
        userInput = input(":")
        if(userInput != "exit"): 
            logThis(writeToArduino("raise"))
            sleep(6.5)
            logThis("arm has been raised")
            logThis("Picture Will Be Taken")
            takePicture()
            logThis("Picture Taken")
            movePicture()
            logThis(writeToArduino("lower"))
            logThis("arm has been lowered")
            
else:
    if(allowRemote):
        logThis("Allow remote is enabled")
        currentInput = GPIO.input(4)
        lastInput = GPIO.input(4)
        GPIO.output(green, 1)
        while True:
            currentInput = GPIO.input(4)
            if(lastInput != currentInput):
                GPIO.output(red, 1)
                logThis("Remote was pressed")
                if(currentInput != lastInput):
                    logThis(writeToArduino("raise"))
                    sleep(6.5)
                    logThis("arm has been raised")
                    logThis("Picture Will Be Taken")
                    GPIO.output(blue, 1)
                    sleep(1)
                    GPIO.output(blue, 0)
                    sleep(1)
                    GPIO.output(blue, 1)
                    sleep(1)
                    GPIO.output(blue, 0)
                    sleep(1)
                    GPIO.output(blue, 1)
                    sleep(1)
                    GPIO.output(blue, 0)
                    sleep(1)
                    GPIO.output(blue, 1)
                    takePicture()
                    logThis("Picture Taken")
                    movePicture()
                    logThis(writeToArduino("lower"))
                    logThis("arm has been lowered")
                    sleep(10.5)
                    GPIO.output(red, 0)
                    GPIO.output(blue, 0)
                    lastInput = GPIO.input(4)
                    currentInput = GPIO.input(4)
            lastInput = currentInput
            
           
    else:
        logThis("Only commands are allowed to be ran")
        while True:
            GPIO.output(blue, 1)
            GPIO.output(red, 1)
            userInput = input(":")
            if(userInput == "photo"):
                logThis("***DEBUG: Take Photo")
                takePicture()
                logThis("Picture Taken")
                movePicture()
            if(userInput == "raise"):
                logThis("***DEBUG: raising arm")
                logThis(writeToArduino("raise"))
            if(userInput == "lower"):
                logThis("***DEBUG: lower arm")
                logThis(writeToArduino("lower"))
            if(userInput == "light"):
                print("light")
                GPIO.output(red, 0)
                GPIO.output(blue, 0)
                GPIO.output(green, 0)
                sleep(3)
                GPIO.output(18, 1)
                sleep(1)
                GPIO.output(18, 0)
                GPIO.output(23, 1)
                sleep(1)
                GPIO.output(23, 0)
                GPIO.output(24, 1)
                sleep(1)
                GPIO.output(24, 0)
            if(userInput == "lower" or userInput == "raise"):
                for x in readFromArduino().split(bytes('\n','utf-8')):
                    print(x[0:-1])
        
    
    
