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

void Face::setExpression(FaceExpression expr) {
    if (expr == _targetExpression && !_animating) return;
    
    _targetExpression = expr;
    
    // Animations that need step-by-step updates
    if (expr == BLINK || expr == SAY) {
        startAnimation(expr);
    } else {
        _animating = false;
        _currentExpression = expr;
    }
}

void Face::startAnimation(FaceExpression expr) {
    _animating = true;
    _animStep = 0;
    _lastAnimTime = millis();
}

void Face::update() {
    unsigned long now = millis();
    
    if (_animating) {
        if (_targetExpression == BLINK) {
            updateBlink();
        } else if (_targetExpression == SAY) {
            updateSay();
        }
    } else {
        // Static expressions - only update if needed
        switch(_currentExpression) {
            case NORMAL: showNormal(); break;
            case SHY: showShy(); break;
            case SAD: showSad(); break;
            case HAPPY: showHappy(); break;
            case UWU: showUwu(); break;
            default: showNormal(); break;
        }
    }
}

void Face::updateBlink() {
    unsigned long now = millis();
    const int BLINK_INTERVAL = 20; // ms between frames
    
    if (now - _lastAnimTime < BLINK_INTERVAL) return;
    _lastAnimTime = now;
    
    // Blink animation: 30 -> 24 -> 18 -> 12 -> 6 -> 2 -> 6 -> 12 -> 18 -> 24 -> 30
    const int blinkHeights[] = {30, 24, 18, 12, 6, 2, 6, 12, 18, 24, 30};
    const int blinkSteps = 11;
    
    if (_animStep < blinkSteps) {
        _eyes.drawNormal(blinkHeights[_animStep]);
        _animStep++;
    } else {
        // Animation finished
        _animating = false;
        _currentExpression = NORMAL;
        _targetExpression = NORMAL;
    }
}

void Face::updateSay() {
    unsigned long now = millis();
    
    // Timing for each frame: frame, duration
    // Frame sequence: 1(80ms), 2(100ms), 1(80ms), 0(100ms), normal
    const int sayFrames[] = {1, 2, 1, 0};
    const int sayDurations[] = {80, 100, 80, 100};
    const int saySteps = 4;
    
    if (_animStep == 0 && now - _lastAnimTime == 0) {
        // First frame
        _eyes.drawNormal();
        _mouth.drawTalk(sayFrames[0]);
        _lastAnimTime = now;
        _animStep = 1;
        return;
    }
    
    if (_animStep > 0 && _animStep <= saySteps) {
        int prevStep = _animStep - 1;
        if (now - _lastAnimTime >= sayDurations[prevStep]) {
            _lastAnimTime = now;
            if (_animStep < saySteps) {
                _mouth.drawTalk(sayFrames[_animStep]);
                _animStep++;
            } else {
                // Animation finished
                _mouth.drawNormal();
                _animating = false;
                _currentExpression = NORMAL;
                _targetExpression = NORMAL;
            }
        }
    }
}