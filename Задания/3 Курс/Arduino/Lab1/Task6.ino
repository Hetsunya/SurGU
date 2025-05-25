// Светодиод подключенный к пину D0 меняет яркость при повороте потенциометра подключенного к пину D1 с частотой 60Гц (ШИМ-сигнал).

void setup() {
  pinMode(D0, OUTPUT);
  analogWriteFreq(120);
}

void loop() {
  int potValue = analogRead(A0);
  int brightness = map(potValue, 0, 4095, 0, 255);
  analogWrite(D0, brightness);
}