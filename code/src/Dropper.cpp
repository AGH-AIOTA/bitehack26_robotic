#include "Dropper.h"
#include <Arduino.h>

Dropper::Dropper(int start, int stop) : startPos(start), stopPos(stop), _currentPos(start) {}

void Dropper::begin(int pin) {
    servo.attach(pin, 500, 2400);
    reset();
}

void Dropper::drop() {
    if (_dropping) return;  // Already dropping
    _dropping = true;
    _waiting = false;
    _currentPos = startPos;
    _lastMoveTime = millis();
}

void Dropper::reset() {
    servo.write(startPos);
    _currentPos = startPos;
    _dropping = false;
    _waiting = false;
}

void Dropper::update() {
    if (!_dropping) return;
    
    unsigned long now = millis();
    
    if (_waiting) {
        // Waiting at bottom position
        if (now - _waitStartTime >= 3000) {
            _waiting = false;
            reset();
        }
        return;
    }
    
    // Moving down
    servo.write(stopPos);
    _waiting = true;
    _waitStartTime = now;
}