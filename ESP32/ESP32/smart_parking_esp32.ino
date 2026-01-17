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
const int greenLEDs[NUM_PARKING]  = {5, 17, 16, 4};
const int redLEDs[NUM_PARKING]    = {2, 15, 13, 12};

bool gateBusy = false;   // لمنع التكرار

void setup() {
  Serial.begin(9600);

  // LCD
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("PARKING STATUS");

  // Servo
  gateServo.attach(SERVO_PIN);
  gateServo.write(90); // مغلق

  // Sensors & LEDs
  for (int i = 0; i < NUM_PARKING; i++) {
    pinMode(sensorPins[i], INPUT_PULLDOWN);
    pinMode(greenLEDs[i], OUTPUT);
    pinMode(redLEDs[i], OUTPUT);
  }

  Serial.println("ESP32 Ready");
}

void loop() {
  int availableCount = 0;

  // ===== قراءة المواقف =====
  for (int i = 0; i < NUM_PARKING; i++) {
    int state = digitalRead(sensorPins[i]);

    if (state == HIGH) {  
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

  // ===== أمر من الكاميرا =====
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "OPEN") {
      if (availableCount > 0 && !gateBusy) {
        openGate();
      } else {
        Serial.println("❌ Parking Full - Gate Closed");
      }
    }
  }

  delay(300);
}

void openGate() {
  gateBusy = true;
  Serial.println("✅ Gate Opening");

  gateServo.write(0);    // فتح
  delay(4000);           // 4 ثواني
  gateServo.write(90);   // إغلاق

  gateBusy = false;
}
