#ifndef CAMERA_MOUNT_H
#define CAMERA_MOUNT_H

#include <ESP32Servo.h>

class CameraMount {
  private:
    Servo servoPan;
    Servo servoTilt;
    int panPos, tiltPos;
    const int stepSize = 2;
    const int deadzone = 15;
    const int centerX = 160; // 320/2
    const int centerY = 120; // 240/2

  public:
    CameraMount();
    void begin(int panPin, int tiltPin);
    void updateTracking(int x, int y);
    void center();
};

#endif