#ifndef FACE_H
#define FACE_H

#include "Eyes.h"
#include "Mouth.h"

class Face {
public:
    Face(uint8_t eyesAddr, uint8_t mouthAddr);
    void begin();
    void showNormal();
    void showBlink();
    void showShy();
    void showSad();
    void showHappy();
    void say(int durationMs);

private:
    Eyes _eyes;
    Mouth _mouth;
};

#endif