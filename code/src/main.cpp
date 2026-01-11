#include <Arduino.h>
#include "communication.h"
#include "Face.h"
#include "Dropper.h"
#include "CameraMount.h"

RPIComm rpiComm = RPIComm();
Face face(0x3D, 0x3C);
Dropper dropper(140, 10);
CameraMount mount;

int tiltPin = 13;
int panPin = 14;

void rpiCallback(Packet packet) {
  Serial.println(String(packet.messageType) + " | " + String(packet.data.servo.x));
  switch(packet.messageType) {
    case DISPLAY_FACES:
      face.setExpression((FaceExpression)packet.data.face);
      break;
    case DROP:
      dropper.drop();
      break;
    case CAMERA_MOUNT:
      mount.updateTracking(packet.data.servo.x, packet.data.servo.y);
      break;
  }
}

void setup() {
  Wire.begin(21, 22);
  face.begin();
  mount.begin(panPin, tiltPin);
  dropper.begin(12); 
  mount.center();
  rpiComm.setPacketCallback(rpiCallback);
  rpiComm.sendLogs(true);
  rpiComm.begin(); 
}

void loop() {
  rpiComm.handle();
  face.update();
  dropper.update();
}