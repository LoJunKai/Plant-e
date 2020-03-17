#include <stdio.h>
float sensorValue = 0; 

int dry = 1040;
int wet = 400; //prevly 30
int moisture = 0;

int sensors[6] = {A0, A1, A2, A3, A4, A5};
float averages[6] = {0};

void setup() { 
 Serial.begin(9600);
} 

void loop() { 
 for (int j = 0; j<6; j++) {
  for (int i = 0; i <= 100; i++) 
    { 
     sensorValue = sensorValue + analogRead(sensors[j]); 
     delay(1); 
    } 
    
    sensorValue = sensorValue/100.0; 
    //Serial.println(sensorValue);
    moisture = ((dry - sensorValue)/(dry - wet)) * 100;
    averages[j] = moisture;
    delay(1000); 
    
    }

 char printstr[11] = {};
 for (int i = 0; i<11; i++){
  if (i%2 == 0){
    printstr[i] = (char) averages[i/2];
  } else {
    printstr[i] = ' ';
  }
 }
 
 Serial.println(printstr);
 
}
