#include <LiquidCrystal.h>
#include <ESP32Servo.h>

// ================= LCD =================
LiquidCrystal lcd(14, 27, 26, 25, 33, 32);

// ================= Servo =================
Servo gateServo;
#define SERVO_PIN 18

// ================= Parking =================
#define NUM_PARKING 4

const int sensorPins[NUM_PARKING] = {23, 22, 21, 19};
const int greenLEDs[NUM_PARKING]  = {5, 12, 17, 16};
const int redLEDs[NUM_PARKING]    = {4, 2, 15, 13};

bool gateOpen = false;

// ================= Setup =================
void setup() {
  Serial.begin(9600);

  // Servo
  gateServo.attach(SERVO_PIN);
  gateServo.write(90); // مغلق

  // LCD
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("PARKING STATUS");

  // Sensors & LEDs
  for (int i = 0; i < NUM_PARKING; i++) {
    pinMode(sensorPins[i], INPUT_PULLDOWN);
    pinMode(greenLEDs[i], OUTPUT);
    pinMode(redLEDs[i], OUTPUT);
  }

  Serial.println("ESP32 Ready");
}

// ================= Loop =================
void loop() {

  int availableCount = 0;
  bool parkingState[NUM_PARKING];

  // ===== قراءة السنسورات (مرة وحدة فقط) =====
  for (int i = 0; i < NUM_PARKING; i++) {
    parkingState[i] = digitalRead(sensorPins[i]);

    if (parkingState[i] == HIGH) {
      digitalWrite(greenLEDs[i], HIGH);
      digitalWrite(redLEDs[i], LOW);
      availableCount++;
    } else {
      digitalWrite(greenLEDs[i], LOW);
      digitalWrite(redLEDs[i], HIGH);
    }
  }

  // ===== LCD =====
  lcd.setCursor(0, 1);
  lcd.print("                ");

  lcd.setCursor(0, 1);
  if (availableCount > 0) {
    lcd.print("Available: ");
    lcd.print(availableCount);
  } else {
    lcd.print("Parking Full");
  }

  // ===== أمر الكاميرا =====
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "OPEN") {
      if (availableCount > 0 && !gateOpen) {
        openGate();
      } else {
        Serial.println("🚫 Parking Full");
      }
    }
  }

  delay(300);
}

// ================= Servo =================
void openGate() {
  gateOpen = true;

  gateServo.write(0);    // فتح
  delay(3000);
  gateServo.write(90);   // إغلاق

  gateOpen = false;
}
