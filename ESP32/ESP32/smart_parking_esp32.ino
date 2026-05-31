#include <LiquidCrystal.h>
#include <ESP32Servo.h>
#include <WiFi.h>
#include <HTTPClient.h>

// ================= WIFI =================
const char* ssid = "Yasmeen";
const char* password = "12345677";

// ================= SERVER =================
String server = "http://172.18.231.11:8000";

// ================= LCD =================
LiquidCrystal lcd(14, 27, 26, 25, 33, 32);

// ================= SERVO =================
Servo gateServo;
#define SERVO_PIN 18

// ================= PARKING =================
#define NUM_PARKING 4

const int sensorPins[NUM_PARKING] = {23, 22, 21, 19};
const int greenLEDs[NUM_PARKING]  = {5, 12, 17, 16};
const int redLEDs[NUM_PARKING]    = {4, 2, 15, 13};

// ================= STATES =================
bool lastState[NUM_PARKING];
bool needSend[NUM_PARKING] = {false};
String pendingStatus[NUM_PARKING];

bool gateOpen = false;

// ================= DISPLAY MODE =================
String systemMode = "STATUS";

// ================= MESSAGE TIMER =================
unsigned long messageStartTime = 0;
const unsigned long MESSAGE_DURATION = 7000; // 7 seconds

// ================= SETUP =================
void setup() {

  Serial.begin(9600);
  Serial.setTimeout(10);

  WiFi.begin(ssid, password);

  lcd.begin(16,2);
  lcd.clear();
  lcd.print("Connecting WiFi");

  int tries = 0;

  while (WiFi.status() != WL_CONNECTED && tries < 30) {
    delay(500);
    tries++;
  }

  lcd.clear();
  lcd.print("PARKING READY");

  gateServo.attach(SERVO_PIN);
  gateServo.write(90);

  for (int i = 0; i < NUM_PARKING; i++) {

    pinMode(sensorPins[i], INPUT_PULLDOWN);

    pinMode(greenLEDs[i], OUTPUT);
    pinMode(redLEDs[i], OUTPUT);

    lastState[i] = digitalRead(sensorPins[i]);
  }
}

// ================= LOOP =================
void loop() {

  int availableCount = 0;

  // ================= READ SENSORS =================
  for (int i = 0; i < NUM_PARKING; i++) {

    bool state = digitalRead(sensorPins[i]);

    if (state == HIGH) {

      digitalWrite(greenLEDs[i], HIGH);
      digitalWrite(redLEDs[i], LOW);
      availableCount++;

    } else {

      digitalWrite(greenLEDs[i], LOW);
      digitalWrite(redLEDs[i], HIGH);
    }

    if (state != lastState[i]) {

      pendingStatus[i] = (state == HIGH) ? "available" : "occupied";
      needSend[i] = true;

      lastState[i] = state;

      if (state == HIGH) {
        Serial.println("LINK_REQUEST:" + String(i + 1));
      }
    }
  }

  // ================= SEND TO SERVER =================
  for (int i = 0; i < NUM_PARKING; i++) {

    if (needSend[i]) {

      sendToServer(i + 1, pendingStatus[i]);
      needSend[i] = false;
    }
  }

  // ================= SERIAL COMMANDS =================
  if (Serial.available()) {

    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "OPEN") {

      systemMode = "OPEN";
      messageStartTime = millis();

      if (availableCount > 0 && !gateOpen) {
        openGate();
      }

    }
    else if (cmd == "REGISTER") {

      systemMode = "REGISTER";
      messageStartTime = millis();

    }
    else if (cmd == "FULL") {

      systemMode = "FULL";
      messageStartTime = millis();
    }
  }

  // ================= AUTO RETURN TO STATUS =================
  if (systemMode != "STATUS") {

    if (millis() - messageStartTime >= MESSAGE_DURATION) {

      systemMode = "STATUS";
    }
  }

  // ================= LCD DISPLAY =================
  lcd.clear();

  if (systemMode == "STATUS") {

    lcd.setCursor(0,0);
    lcd.print("PARKING STATUS");

    lcd.setCursor(0,1);

    if (availableCount > 0) {

      lcd.print("Available:");
      lcd.print(availableCount);

    } else {

      lcd.print("FULL");
    }
  }

  else if (systemMode == "REGISTER") {

    lcd.setCursor(0,0);
    lcd.print("REG REQUIRED");

    lcd.setCursor(0,1);
    lcd.print("SCAN QR");
  }

  else if (systemMode == "FULL") {

    lcd.setCursor(0,0);
    lcd.print("PARKING FULL");
  }

  else if (systemMode == "OPEN") {

    lcd.setCursor(0,0);
    lcd.print("ACCESS GRANTED");
  }

  delay(300);
}

// ================= HTTP SEND =================
void sendToServer(int spot, String status) {

  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;

  String url = server + "/spot/" + String(spot) + "?status=" + status;

  http.begin(url);
  http.setTimeout(2000);

  int code = http.PUT("");

  Serial.print("Spot ");
  Serial.print(spot);
  Serial.print(" => ");
  Serial.println(code);

  http.end();
}

// ================= SERVO =================
void openGate() {

  gateOpen = true;

  gateServo.write(0);
  delay(1800);

  gateServo.write(90);

  gateOpen = false;
}
