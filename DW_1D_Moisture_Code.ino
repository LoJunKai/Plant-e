#define SensorPin A0 
#include <stdio.h>
float sensorValue = 0; 
int dry = 1040;
int wet = 30;
int moisture = 0;

void setup() { 
 Serial.begin(9600); 
} 

void loop() { 
 for (int i = 0; i <= 100; i++) 
 { 
   sensorValue = sensorValue + analogRead(SensorPin); 
   delay(1); 
 } 
 sensorValue = sensorValue/100.0; 
 moisture = ((dry - sensorValue)/(dry - wet)) * 100;
 Serial.println(moisture);
 delay(1000); 
} 
