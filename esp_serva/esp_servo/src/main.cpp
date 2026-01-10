#include <Arduino.h>
#include "Dropper.h"
#include "CameraMount.h"

// Inicjalizacja obiektów
Dropper dropper(140, 10);
CameraMount mount;

void setup() {
    Serial.begin(115200);
    
    // Uruchomienie modułów (piny: Pan=13, Tilt=12, Dropper np. 14)
    mount.begin(14, 12);
    dropper.begin(13); 

    Serial.println("System gotowy.");
}

void loop() {
    // if (Serial.available() > 0) {
        // Przykładowa logika: jeśli coś przyjdzie na Serial, zrzuć
        dropper.drop();
        delay(2000);
        dropper.reset();
    // }
    
    // Tu możesz wywoływać mount.updateTracking(x, y) 
    // po odebraniu współrzędnych z kamery
}