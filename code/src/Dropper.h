#ifndef DROPPER_H
#define DROPPER_H

#include <ESP32Servo.h>

class Dropper {
  private:
    Servo servo;
    int startPos;
    int stopPos;
    
    // Non-blocking state
    bool _dropping = false;
    bool _waiting = false;
    int _currentPos;
    unsigned long _lastMoveTime = 0;
    unsigned long _waitStartTime = 0;

  public:
    Dropper(int start, int stop);
    void begin(int pin);
    void drop();
    void reset();
    void update();  // Non-blocking update, call in loop
    bool isDropping() const { return _dropping; }
};

#endif