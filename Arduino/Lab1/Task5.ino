// Реализовать задание из пункта №3, но с использованием встроенного аппаратного таймера вместо нажатия на кнопку;
#include "pico.h"
#include "hardware/timer.h"

const int ledPins[] = {D0, D1, D2};
const long interval = 5000;  // Интервал между сменой светодиода

struct repeating_timer MyTimer;
volatile int currentLED = 0;

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  add_repeating_timer_ms(3000, Timer, nullptr, &MyTimer);
}

bool Timer(struct repeating_timer *t) {
  digitalWrite(ledPins[currentLED], LOW);
  currentLED = (currentLED + 1) % 3;
  digitalWrite(ledPins[currentLED], HIGH);
  return true;
}

void loop() {
}