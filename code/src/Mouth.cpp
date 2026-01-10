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
    _display.fillRect(46, 31, 36, 3, SSD1306_WHITE);
    _display.display();
}

void Mouth::drawShy() {
    _display.clearDisplay();
    _display.drawCircle(64, 32, 12, SSD1306_WHITE);
    _display.display();
}

void Mouth::drawSad() {
    _display.clearDisplay();
    _display.drawCircle(64, 50, 22, SSD1306_WHITE);
    _display.fillRect(0, 45, 128, 19, SSD1306_BLACK); 
    _display.display();
}

void Mouth::drawHappy() {
    _display.clearDisplay();
    _display.drawCircle(64, 18, 28, SSD1306_WHITE);
    _display.fillRect(0, 0, 128, 22, SSD1306_BLACK); 
    _display.display();
}

void Mouth::drawTalk(int frame) {
    _display.clearDisplay();
    if (frame == 0) {
        // Zamknięte (linia)
        _display.fillRect(45, 31, 38, 3, SSD1306_WHITE);
    } else if (frame == 1) {
        // Półotwarte (mała elipsa)
        _display.fillRoundRect(40, 25, 48, 14, 6, SSD1306_WHITE);
    } else {
        // Szeroko otwarte (duże koło/elipsa)
        _display.fillRoundRect(35, 18, 58, 28, 14, SSD1306_WHITE);
    }
    _display.display();
}

void Mouth::drawUwu() {
    _display.clearDisplay();
    // Rysuje większe 'w' - bardziej wyraźne usta UwU
    // Lewe ukośne
    _display.drawLine(45, 26, 56, 36, SSD1306_WHITE);
    _display.drawLine(46, 26, 57, 36, SSD1306_WHITE);
    // Środkowe dołek
    _display.drawLine(56, 36, 64, 30, SSD1306_WHITE);
    _display.drawLine(57, 36, 64, 31, SSD1306_WHITE);
    // Prawe ukośne
    _display.drawLine(64, 30, 72, 36, SSD1306_WHITE);
    _display.drawLine(64, 31, 71, 36, SSD1306_WHITE);
    _display.drawLine(72, 36, 83, 26, SSD1306_WHITE);
    _display.drawLine(71, 36, 82, 26, SSD1306_WHITE);
    _display.display();
}