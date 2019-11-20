from time import sleep
import serial
from goprocam import GoProCamera
from goprocam import constants
import RPi.GPIO as GPIO    


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    

GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
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
    TIMER=4
    gpCam.downloadLastMedia(gpCam.take_photo(TIMER)) #take a photo in 4 seconds and download it.
    print("Picture has been taken and downloaded.")

lastInput = 0
while (True):
    userInput = ""
    currentInput = GPIO.input(4)
    if(lastInput != currentInput):
        GPIO.output(18, currentInput)
        print("The button was pressed.")
        if(currentInput == 0):
            print(writeToArduino("raise"))

        else:
            print(writeToArduino("lower"))

        #print(writeToArduino("raise"))
        #for x in readFromArduino().split(bytes('\n','utf-8')):
        #    print(x[0:-1])
    else:
    #userInput = input(":")
        if(userInput == "raise" or userInput == "lower" or userInput == "r" or userInput == "l" or lastInput != currentInput):

            print(writeToArduino(userInput))
            for x in readFromArduino().split(bytes('\n','utf-8')):
                print(x[0:-1])
        if(userInput == "photo"):
            takePicture()
    lastInput = currentInput


