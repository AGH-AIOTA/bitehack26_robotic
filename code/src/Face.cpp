#include "Face.h"
#include <Arduino.h>

Face::Face(uint8_t eyesAddr, uint8_t mouthAddr) 
    : _eyes(eyesAddr), _mouth(mouthAddr) {}

void Face::begin() {
    _eyes.begin();
    _mouth.begin();
}

void Face::showNormal() {
    _mouth.drawNormal();
    _eyes.drawNormal();
}

void Face::showBlink() {
    for(int h=30; h>2; h-=6) _eyes.drawNormal(h); 
    for(int h=2; h<=30; h+=6) _eyes.drawNormal(h);
}

void Face::showShy() {
    _eyes.drawShy();
    _mouth.drawShy();
}

void Face::showSad() {
    _eyes.drawSad();
    _mouth.drawSad();
}

void Face::showHappy() {
    _eyes.drawHappy();
    _mouth.drawHappy();
}

void Face::showUwu() {
    _eyes.drawUwu();
    _mouth.drawUwu();
}

void Face::say(int durationMs) {
    unsigned long startTime = millis();
    _eyes.drawNormal(); // Oczy patrzą normalnie podczas mówienia

    while (millis() - startTime < durationMs) {
        _mouth.drawTalk(1); delay(80);
        _mouth.drawTalk(2); delay(100);
        _mouth.drawTalk(1); delay(80);
        _mouth.drawTalk(0); delay(100);
    }
    _mouth.drawNormal(); // Zamknij usta po zakończeniu
}