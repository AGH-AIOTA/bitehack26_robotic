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
    const int centerX = 320; // 640/2
    const int centerY = 240; // 480/2

  public:
    CameraMount();
    void begin(int panPin, int tiltPin);
    void updateTracking(int16_t x, int16_t y);
    void center();
};

#endif