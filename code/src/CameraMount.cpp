#include "CameraMount.h"
#include <Arduino.h>

CameraMount::CameraMount() : panPos(90), tiltPos(90) {}

void CameraMount::begin(int panPin, int tiltPin) {
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    servoPan.attach(panPin, 500, 2400);
    servoTilt.attach(tiltPin, 500, 2400);
    center();
}

void CameraMount::center() {
    panPos = 90;
    tiltPos = 90;
    servoPan.write(panPos);
    servoTilt.write(tiltPos);
}

void CameraMount::updateTracking(int x, int y) {
    if (x < (centerX - deadzone)) panPos += stepSize;
    else if (x > (centerX + deadzone)) panPos -= stepSize;

    if (y < (centerY - deadzone)) tiltPos -= stepSize;
    else if (y > (centerY + deadzone)) tiltPos += stepSize;

    panPos = constrain(panPos, 0, 180);
    tiltPos = constrain(tiltPos, 0, 180);

    servoPan.write(panPos);
    servoTilt.write(tiltPos);
}