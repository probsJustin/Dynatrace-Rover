# DevOne Detroit Rover

Repo for all scripts/code/models related to the DevOne Rover. Both testing and final scripts/models are located in this repo. 

By: Justin Hagerty 
Note Last Edit: 11/15/2019
### Credits: 

Arnaud Crowther, Chris Anders, Dan Dyla, and Tom Carrio. 

### Hardware: 
 - Arduino 2560 Mega
 - Raspberry Pi3
 - TB6650 Stepper Motor Drivers
 - Nema23 stepper motors(426in/oz)
 - GoPro Session 4
 - Dual Network Interface/s for RPI (common problem/road block for RPI which is why it is mentioned).
 - RF wireless relay

## Overview: 

From a user’s perspective: User presses a button on a rf remote that sends a rf signal to a relay that completes a circuit for the raspberry pi to let it know that the button was pressed. Raspberry pi sends a serial message to the Arduino telling it to raise the arm - the Arduino sends a PWM to the stepper motor drivers to tell them to raise the motor. At the Raspberry Pi level we get ready to trigger the Go Pro and take the picture - once the arm is raised the picture is taken and at the same time the raspberry pi changes the name of the picture replacing the old "image.png" with the new photo and triggers the node/twitter command to upload the picture up to twitter. 


## Post Mortem of Rover: 

Demo Day: There were a couple of problems with transporting such a frail project. The plastic took many hours to print even at a cost to strength. Not only is the rover very difficult to pack up and transport but one the way to the venue the rover broke due to a roll over in the vehicle. I had thought ahead and printed some spare parts to ensure that if anything broke that was structurally needed that we would still be able to use the rover. However, there were a couple of decorative pieces that I did not have backups of because by the time these had been printed, we were already days away from the convention. We ran into a few issues setting up and we were not able to get the rover set up and working with in the first 2 acts due to a networking issue. Tom Carrio and I were able to identify that the Go Pro seemed to have a DNS routing conflict that conflicted with the DNS routing that was set by default for the local network at the venue. I had tried to mitigate any network issues at home testing with multiple networks, but it was difficult to really calculate environmental issues like these. After some time and trouble shooting, we were able to get the rover working just before lunch. It worked for about an hour but due to testing it had significantly drained the battery on the GoPro and stalled the rover mid photo. We recharged the go pro and put it back to work just after lunch. The goPro died one other time but we were able to set it up with a charging cable that also allowed for use of the goPro during its job. After this the rover seemed to work flawlessly for the rest of the convention. It seems that theatrics and environmental issues were the real hang up here. 

### Things that I think went well: 

 - It was not difficult to find libs and information about setting up the go pro for remote use with an API. 
 - I had a lot of the hardware available.
 - Access to a capable 3D printer was not an issue thanks to Chris Anders. 
 - Access to a go pro/s thanks to Dan Dyla. 
 - Access to parts/components that I did not have was also not an issue. 
 - Budgeting (I was worried that this would come in over budget, but I actually was able to keep this to a sub-estimate) 
 - Design (while this was initially a hurdle during prototyping, I feel that once the over design was built it was easy to adjust and add things on)
 - "fake" debug flags that were set in the code to allow for us to test/make changes on the fly. While these were not implemented in a standard way, I feel that it was still helpful during the convention.  

### Things that I think were "difficult" relative to the overall difficulty of the project and or just down right negatives: 
 - Design: It took many iterations in certain cases for me to get the prototyping right for certain parts. Design is not a strong point for me so unfortunately this took a lot of my time as there was a single part on the rover that took less than 3 hours to print. (Initially I wanted to have a several axis arm that used a planetary gear box that I had modified from the engineer "GearDownForWhat”, but I had scrapped that feature due to time constraints.) There was a lot of wasted plastic and it would have been nice to have mitigated this better - I feel as if this could have been helped with a more seasoned design/modeling engineer. I also feel like this was a very poor design - the rover was held together with machine screws at every turn and I feel that these could have been a lot more well-hidden to help give it a more modern feel. I was hoping to have more decorative pieces on the rover as well, but I did not have the time to print and prototype a lot of decorative pieces as the goal was features and functions then decoration and esthetics. 
 - Dual Wi-Fi interfaces were needed to ensure that connectivity to the internet for twitter as well as connectivity to the local go pro to allow for use of the API. This is semi difficult to accomplish with the RPI as it does not out right "support" this without any modification by this I mean that it is different than the normal Debian/ubuntu variants of Linux and it took some doing to force it to connect correctly. Ultimately this did not take much time, but this was a foreseen and mitigated problem that I knew going into the build. 
 - Time: I did not have a lot of time to really get the software end of this done. The prototyping and design work took up most of the build time. However, this was also a foreseen problem that I attempted to mitigate by trying to find an alternative to 3D printing the entire body and frame. I had originally decided that it would be better served to use a bit of insulating foam to fill and structure the rover body and hold parts in place. I was not able to find a good pack foam that would allow for this kind of structure/rapid development as it would cost almost no time to allow for more development of the arm and possibly a second and third axis. (everyone loves moving parts.) Each piece of the rover took a significant amount of time to print and changes were made to each piece as the rover design/build went on. At no point was a part "set in stone". By the time I had the rover to a state where I could focus on the software end of this it was already rather close to the deadline. I also knew ahead of time that this would like to take the "least amount of time" and it was a point in the project where I had the most flexibility to recuperate time from the design phase if we were close to the deadline (what was the case.) 
 - Error handling/Exception handling - there was a lack of such in the software for the rover and I feel that this *should* have been handled. 
 - Threading - despite the project being rather small and having a very small requirement as far as computing and resources goes; I feel that this should have had a multi-threaded or "pythonic async single thread/multi thread" methods to allow for better communication between all the parts of the rover - this would have potentially allowed for status lighting and communication between the rover and the user. This also would allow for even better logging, error handling and status messages. 
 - More features: I feel like the rover should have had more features - I feel like this could have been accomplished if there were less time constraints. 


README FOR NODE TWITTER MECHANISM: 

## Twitter API Interface
Credit: Arnaud Crowther for the twitter mechanism.
### Requirements
- Node (latest)
- Network connection
- Environment file `.env`

### Get started
- Install dependencies: `$ npm i`
- Add an image to root named `"image.png"`
- Run app: `$ node post`
- Overwrite new image with same name
- Repeat run: `$ node post`
