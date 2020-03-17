#include <stdio.h>
float sensorValue = 0; 

int dry = 500;
int wet = 0; //prevly 30
int moisture = 0;

int sensors[6] = {A0, A1, A2, A3, A4, A5};

void setup() { 
  Serial.begin(9600);
} 

void loop() { 
  if (Serial.available())
  {
    int plant = Serial.parseInt();
    
    // Take 100 readings and take the average
    for (int i = 0; i <= 100; i++)
    { 
     sensorValue = sensorValue + analogRead(sensors[plant]); 
     delay(1); 
    }
    sensorValue = sensorValue/100.0;
    
    moisture = ((dry - sensorValue)/(dry - wet)) * 100;
    if (moisture > 100)
    {
      moisture = 100;
    } 
    else if (moisture < 0)
    {
      moisture = 0;
    }
    
    Serial.println( (char) moisture);
  }
}
