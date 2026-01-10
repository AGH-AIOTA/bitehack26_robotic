#include "Eyes.h"

Eyes::Eyes(uint8_t addr) : _display(128, 64, &Wire, -1), _addr(addr) {}

bool Eyes::begin() {
    if (!_display.begin(_addr, true)) return false;
    _display.setContrast(255);
    return true;
}

void Eyes::drawNormal(int h) {
    _display.clearDisplay();
    _display.fillRoundRect(30, 32 - (h/2), 25, h, 8, SH110X_WHITE);
    _display.fillRoundRect(73, 32 - (h/2), 25, h, 8, SH110X_WHITE);
    _display.display();
}

void Eyes::drawShy() {
    _display.clearDisplay();
    _display.drawLine(30, 25, 50, 35, SH110X_WHITE); _display.drawLine(30, 45, 50, 35, SH110X_WHITE);
    _display.drawLine(95, 25, 75, 35, SH110X_WHITE); _display.drawLine(95, 45, 75, 35, SH110X_WHITE);
    for(int i=0; i<4; i++) {
        _display.drawLine(25+(i*5), 50, 30+(i*5), 58, SH110X_WHITE);
        _display.drawLine(85+(i*5), 50, 90+(i*5), 58, SH110X_WHITE);
    }
    _display.display();
}

void Eyes::drawSad() {
    _display.clearDisplay();
    _display.fillRoundRect(30, 28, 25, 25, 8, SH110X_WHITE);
    _display.fillRoundRect(73, 28, 25, 25, 8, SH110X_WHITE);
    _display.fillTriangle(30, 28, 60, 28, 30, 45, SH110X_BLACK); 
    _display.fillTriangle(73, 28, 103, 28, 103, 45, SH110X_BLACK);
    _display.display();
}

void Eyes::drawHappy() {
    _display.clearDisplay();
    _display.fillCircle(42, 40, 15, SH110X_WHITE);
    _display.fillCircle(85, 40, 15, SH110X_WHITE);
    _display.fillRect(0, 40, 128, 25, SH110X_BLACK); 
    _display.display();
}