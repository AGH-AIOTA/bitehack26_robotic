#include "Eyes.h"

Eyes::Eyes(uint8_t addr) : _display(128, 64, &Wire, -1), _addr(addr) {}

bool Eyes::begin() {
    if (!_display.begin(_addr, true)) return false;
    _display.setContrast(255);
    return true;
}

void Eyes::drawNormal(int h) {
    _display.clearDisplay();
    _display.fillRoundRect(10, 32 - (h/2), 45, h, 12, SH110X_WHITE);
    _display.fillRoundRect(73, 32 - (h/2), 45, h, 12, SH110X_WHITE);
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
    _display.fillRoundRect(10, 15, 45, 45, 12, SH110X_WHITE);
    _display.fillRoundRect(73, 15, 45, 45, 12, SH110X_WHITE);
    _display.fillTriangle(10, 15, 60, 15, 10, 55, SH110X_BLACK); 
    _display.fillTriangle(73, 15, 123, 15, 123, 55, SH110X_BLACK);
    _display.display();
}

void Eyes::drawHappy() {
    _display.clearDisplay();
    _display.fillCircle(32, 36, 26, SH110X_WHITE);
    _display.fillCircle(96, 36, 26, SH110X_WHITE);
    _display.fillRect(0, 36, 128, 28, SH110X_BLACK); 
    _display.display();
}

void Eyes::drawUwu() {
    _display.clearDisplay();
    // Lewe oko - grubszy łuk (zamknięte szczęśliwe oko)
    for(int i=0; i<5; i++) {
        _display.drawCircle(30, 42-i, 22, SH110X_WHITE);
    }
    _display.fillRect(0, 0, 60, 25, SH110X_BLACK);
    
    // Prawe oko - grubszy łuk (zamknięte szczęśliwe oko)
    for(int i=0; i<5; i++) {
        _display.drawCircle(98, 42-i, 22, SH110X_WHITE);
    }
    _display.fillRect(68, 0, 60, 25, SH110X_BLACK);
    
    // Rumieńce - małe kółka pod oczami
    _display.fillCircle(15, 40, 4, SH110X_WHITE);
    _display.fillCircle(113, 40, 4, SH110X_WHITE);
    
    _display.display();
}