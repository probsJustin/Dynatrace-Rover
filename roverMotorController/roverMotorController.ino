#include <AccelStepper.h>
#include <MultiStepper.h>

AccelStepper stepper2(AccelStepper::FULL2WIRE, 3,2); 
AccelStepper stepper3(AccelStepper::FULL2WIRE, 11, 10);
String incomingMessage = 0; // for incoming serial data

void setup()
{  
    Serial.begin(9600); 
    Serial.println("[Rover] Starting....");
    stepper2.setMaxSpeed(300.0);
    stepper2.setAcceleration(100.0);
    
    stepper3.setMaxSpeed(300.0);
    stepper3.setAcceleration(100.0);
    
    stepper3.moveTo(1);
    stepper2.moveTo(1);
    stepper2.run();
    stepper3.run();    
}
void loop()
{
    if(Serial.available() > 0){
    incomingMessage = Serial.readString();  
    Serial.println("repeat :" + incomingMessage);
        Serial.println("[Rover] arm has stopped moving....");
        if(incomingMessage == "raise"){
          Serial.println("[Rover] raising arm....");
          stepper3.moveTo(stepper2.currentPosition() - 1800);
          stepper2.moveTo(stepper3.currentPosition() - 1800);

        }
        if(incomingMessage == "lower"){
          Serial.println("[Rover] lowering arm....");
          stepper3.moveTo(stepper2.currentPosition() + 1800);
          stepper2.moveTo(stepper3.currentPosition() + 1800);

        }
        if(incomingMessage == "r"){
          Serial.println("[Rover] raising arm....");
          stepper3.moveTo(stepper2.currentPosition() - 50);
          stepper2.moveTo(stepper3.currentPosition() - 50);

        }
        if(incomingMessage == "l"){
          Serial.println("[Rover] lowering arm....");
          stepper3.moveTo(stepper2.currentPosition() + 50);
          stepper2.moveTo(stepper3.currentPosition() + 50);

        }
        
    }
    
    // Change direction at the limits
    //if (stepper2.distanceToGo() == 0)
    //    stepper2.moveTo(-stepper2.currentPosition());
    //if (stepper3.distanceToGo() == 0)
    //   stepper3.moveTo(-stepper3.currentPosition());
   
    stepper2.run();
    stepper3.run();
}
