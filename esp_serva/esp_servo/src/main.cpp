#include <Arduino.h>
#include <ESP32Servo.h>

Servo servoPan;  // Poziom
Servo servoTilt; // Pion

const int panPin = 13;
const int tiltPin = 12;

// --- KONFIGURACJA ---
int panPos = 90; // Startowa pozycja środkowa
int tiltPos = 90;
const int stepSize = 2;   // Jak szybko serwo ma się obracać (w stopniach)
const int deadzone = 15;  // Tolerancja błędu w pikselach (twarz "prawie" na środku)

// Rozdzielczość wirtualnej kamery (standard dla ESP32-CAM)
const int camWidth = 320;
const int camHeight = 240;
const int centerX = camWidth / 2;
const int centerY = camHeight / 2;

void updateTracking(int x, int y);

void setup() {
  Serial.begin(115200);
  
  // Konfiguracja serw
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  servoPan.attach(panPin, 500, 2400);
  servoTilt.attach(tiltPin, 500, 2400);

    // Ustawienie na start
  servoPan.write(panPos);
  servoTilt.write(tiltPos);

  // 1. Ruch w poziomie (Pan)
    Serial.println("Ruch Pan: 0 -> 180");
    for (int pos = 0; pos <= 180; pos += 1) {
        servoPan.write(pos);
        delay(15);
    }
    
    // 2. Ruch w pionie (Tilt)
    Serial.println("Ruch Tilt: 0 -> 180");
    for (int pos = 0; pos <= 180; pos += 1) {
        servoTilt.write(pos);
        delay(15);
    }

  // Ustawienie na start
  servoPan.write(panPos);
  servoTilt.write(tiltPos);

  Serial.println("System gotowy. Wpisz w Serial Monitorze: X Y (np. 100 150)");
}

void loop() {
  // Symulacja danych z kamery przez Serial Monitor
  if (Serial.available() > 0) {
    int faceX = Serial.parseInt(); // Odczytaj X twarzy
    int faceY = Serial.parseInt(); // Odczytaj Y twarzy
    
    if (faceX > 0 && faceY > 0) {
      updateTracking(faceX, faceY);
    }
  }
}

void updateTracking(int x, int y) {
  // --- LOGIKA POZIOMA (PAN) ---
  if (x < (centerX - deadzone)) {
    panPos += stepSize; // Twarz po lewej -> obróć w lewo
  } else if (x > (centerX + deadzone)) {
    panPos -= stepSize; // Twarz po prawej -> obróć w prawo
  }

  // --- LOGIKA PIONOWA (TILT) ---
  if (y < (centerY - deadzone)) {
    tiltPos -= stepSize; // Twarz u góry -> obróć w górę
  } else if (y > (centerY + deadzone)) {
    tiltPos += stepSize; // Twarz na dole -> obróć w dół
  }

  // Ograniczenie zakresu serw (żeby nie próbowały wyjść poza 0-180)
  panPos = constrain(panPos, 0, 180);
  tiltPos = constrain(tiltPos, 0, 180);

  // Ruch serwa
  servoPan.write(panPos);
  servoTilt.write(tiltPos);

  // Debugging
  Serial.print("Twarz na: "); Serial.print(x); Serial.print(","); Serial.print(y);
  Serial.print(" | Serwa: "); Serial.print(panPos); Serial.print(","); Serial.println(tiltPos);
}