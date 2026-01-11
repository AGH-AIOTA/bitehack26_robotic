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
    void showShy();
    void showSad();
    void showHappy();
    void showUwu();
    void update();  // Non-blocking update, call in loop
    void setExpression(FaceExpression expr);
    bool isAnimating() const { return _animating; }

private:
    Eyes _eyes;
    Mouth _mouth;
    
    // Animation state
    FaceExpression _currentExpression = NORMAL;
    FaceExpression _targetExpression = NORMAL;
    bool _animating = false;
    unsigned long _lastAnimTime = 0;
    int _animStep = 0;
    
    // Animation helpers
    void updateBlink();
    void updateSay();
    void startAnimation(FaceExpression expr);
};

#endif