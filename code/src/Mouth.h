#ifndef MOUTH_H
#define MOUTH_H

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

class Mouth {
public:
    Mouth(uint8_t addr);
    bool begin();
    void drawNormal();
    void drawShy();
    void drawSad();
    void drawHappy();
    void drawTalk(int frame);

private:
    Adafruit_SSD1306 _display;
    uint8_t _addr;
};

#endif