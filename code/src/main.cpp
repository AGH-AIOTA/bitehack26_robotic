#include <Arduino.h>
#include "communication.h"

RPIComm rpiComm = RPIComm();

void rpiCallback(Packet packet) {
  Serial.println(String(packet.messageType) + " | " + String(packet.data.servo.x));
}

void setup() {
  Serial.begin(115200); 
  
  rpiComm.setPacketCallback(rpiCallback);
  rpiComm.sendLogs(true);
  rpiComm.begin(); 
}

void loop() {
  rpiComm.handle();
  delay(10); 
}