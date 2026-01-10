#ifndef DROPPER_H
#define DROPPER_H

#include <ESP32Servo.h>

class Dropper {
  private:
    Servo servo;
    int startPos;
    int stopPos;

  public:
    Dropper(int start, int stop);
    void begin(int pin);
    void drop();
    void reset();
};

#endif