#include "Mouth.h"

Mouth::Mouth(uint8_t addr) : _display(128, 64, &Wire, -1), _addr(addr) {}

bool Mouth::begin() {
    if (!_display.begin(SSD1306_SWITCHCAPVCC, _addr)) return false;
    _display.clearDisplay();
    _display.display();
    return true;
}

void Mouth::drawNormal() {
    _display.clearDisplay();
    _display.fillRect(54, 31, 20, 2, SSD1306_WHITE);
    _display.display();
}

void Mouth::drawShy() {
    _display.clearDisplay();
    _display.drawCircle(64, 32, 8, SSD1306_WHITE);
    _display.display();
}

void Mouth::drawSad() {
    _display.clearDisplay();
    _display.drawCircle(64, 45, 15, SSD1306_WHITE);
    _display.fillRect(0, 42, 128, 22, SSD1306_BLACK); 
    _display.display();
}

void Mouth::drawHappy() {
    _display.clearDisplay();
    _display.drawCircle(64, 20, 20, SSD1306_WHITE);
    _display.fillRect(0, 0, 128, 25, SSD1306_BLACK); 
    _display.display();
}

void Mouth::drawTalk(int frame) {
    _display.clearDisplay();
    if (frame == 0) {
        // Zamknięte (linia)
        _display.fillRect(50, 31, 28, 2, SSD1306_WHITE);
    } else if (frame == 1) {
        // Półotwarte (mała elipsa)
        _display.fillRoundRect(50, 28, 28, 8, 4, SSD1306_WHITE);
    } else {
        // Szeroko otwarte (duże koło/elipsa)
        _display.fillRoundRect(45, 22, 38, 20, 10, SSD1306_WHITE);
    }
    _display.display();
}