#include <Arduino.h>

#include <EEPROM.h>

// Module connection pins (Digital Pins)



// variable use to measuer the intervals inbetween impulses
int i=0;
// Number of impulses detected
int impulsCount=0;
// Sum of all the coins inseted
float total_amount=0;
float verif = total_amount;



void setup() {
 // pinMode(2, INPUT_PULLUP);
 Serial.begin(9600);

 // Interrupt connected to PIN D2 executing IncomingImpuls function when signal goes from HIGH to LOW
 attachInterrupt(0,incomingImpuls, FALLING);
 EEPROM.read(total_amount);
 Serial.print('begin');



}

void incomingImpuls()
{
  impulsCount=impulsCount+1;
  i=0;
}

void loop() {
  i=i+1;
    
  if (i%30 ==0){
    Serial.print(" Total:");
    Serial.print(total_amount);
  }

  if (i>=30 and impulsCount==1){
    total_amount=total_amount+2;
    impulsCount=0;
    EEPROM.read( total_amount);
  }
  if (i>=30 and impulsCount==2){
    total_amount=total_amount+1;
    impulsCount=0;
    EEPROM.read( total_amount);
  }
  if (i>=30 and impulsCount==3){
    total_amount=total_amount+0.5;
    impulsCount=0;
    EEPROM.read( total_amount);
  }
  if (i>=30 and impulsCount==4){
    total_amount=total_amount+0.2;
    impulsCount=0;
    EEPROM.read( total_amount);
  }
  if (i>=30 and impulsCount==5){
    total_amount=total_amount+0.1;
    impulsCount=0;
    EEPROM.read( total_amount);
  }}