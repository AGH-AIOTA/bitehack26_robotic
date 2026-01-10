#include "Dropper.h"
#include <Arduino.h>

Dropper::Dropper(int start, int stop) : startPos(start), stopPos(stop) {}

void Dropper::begin(int pin) {
    servo.attach(pin, 500, 2400);
    reset();
}

void Dropper::drop() {
    for (int pos = startPos; pos >= stopPos; --pos) {
        servo.write(pos);
        if (pos == stopPos) delay(1000);
        else delay(15);
    }
}

void Dropper::reset() {
    servo.write(startPos);
}