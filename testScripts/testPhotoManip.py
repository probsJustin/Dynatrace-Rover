import os
import re
from goprocam import GoProCamera
from goprocam import constants

#when set to true it will not upload the picture to twitter but will leave it on the raspberry pi as image.png
dryRun = True
#if enabled it will allow for the gopro to take the picture and move it to image.png but this is still dependant on the dry run variable
takePhoto = False
#if true this will use the remote as the trigger - if false it will allow for commands to be ran for debug
allowRemote = True
#turn on lights if true
lights = False 


def takePicture():
    gpCam = GoProCamera.GoPro()
    TIMER=4
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
