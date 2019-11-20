from goprocam import GoProCamera
from goprocam import constants

def takePicture():
    gpCam = GoProCamera.GoPro()
    TIMER=4
    gpCam.downloadLastMedia(gpCam.take_photo(TIMER)) #take a photo in 4 seconds and download it.
    print("Picture has been taken and downloaded.")

takePicture()
