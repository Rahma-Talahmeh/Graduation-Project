#include <ESP32Servo.h>

Servo gateServo;

const int IR_PIN  = 34;
const int LED_PIN = 2;
const int LDR_PIN = 35;

bool gateOpen = false;   // لمنع التكرار

void setup() {
  Serial.begin(9600);

  gateServo.attach(18);   // ✅ السيرفو على D18
  gateServo.write(90);     // الحاجز مغلق

  pinMode(IR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(LDR_PIN, INPUT);

  Serial.println("ESP32 Ready");
}

void loop() {

  // ===== 1️⃣ أمر من Python =====
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "OPEN" && !gateOpen) {
      Serial.println("فتح الحاجز من Python");
      openGate();
    }
  }

  // ===== 2️⃣ فتح من IR Sensor =====
  int irValue = digitalRead(IR_PIN);
  if (irValue == HIGH && !gateOpen) {
    Serial.println("جسم تم رصده - فتح الحاجز");
    openGate();
  }

  // ===== LED حسب الإضاءة =====
  int ldrValue = analogRead(LDR_PIN);
  digitalWrite(LED_PIN, ldrValue < 500 ? HIGH : LOW);

  delay(1000);
}
 
void openGate() {
  gateOpen = true;

  gateServo.write(0);          // فتح
  digitalWrite(LED_PIN, HIGH);

  delay(2000);                  // ⏱️ انتظار 4 ثواني

  gateServo.write(90);           // غلق
  digitalWrite(LED_PIN, LOW);

  gateOpen = false;
}