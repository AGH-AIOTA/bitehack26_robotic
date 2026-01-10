#include <Arduino.h>
#include <Wire.h>
#include "Face.h"

// Tworzymy twarz robota
Face face(0x3D, 0x3C);

void setup() {
  Wire.begin(21, 22);
  face.begin();
}

void loop() {
  face.showNormal();
  delay(2000);
  face.showBlink();
  
  delay(1000);
  face.showHappy();
  delay(2000);

  delay(1000);
  face.showSad();
  delay(2000);

  delay(1000);
  face.showShy();
  delay(2000);

  delay(1000);
  face.showHappy();
  face.say(1500);
  
  delay(3000);
}