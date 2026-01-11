#ifndef FACE_H
#define FACE_H

#include "Eyes.h"
#include "Mouth.h"

enum FaceExpression {
    NORMAL,
    BLINK,
    SHY,
    SAD,
    HAPPY,
    UWU,
    SAY
};

class Face {
public:
    Face(uint8_t eyesAddr, uint8_t mouthAddr);
    void begin();
    void showNormal();
    void showBlink();
    void showShy();
    void showSad();
    void showHappy();
    void showUwu();
    void say();
    void showFace(FaceExpression faceExpression);

private:
    Eyes _eyes;
    Mouth _mouth;
};

#endif