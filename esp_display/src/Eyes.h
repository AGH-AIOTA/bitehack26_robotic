#ifndef EYES_H
#define EYES_H

#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

class Eyes {
public:
    Eyes(uint8_t addr);
    bool begin();
    void drawNormal(int h = 30);
    void drawShy();
    void drawSad();
    void drawHappy();
    void drawUwu();

private:
    Adafruit_SH1106G _display;
    uint8_t _addr;
};

#endif