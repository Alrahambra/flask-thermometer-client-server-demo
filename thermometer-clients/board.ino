#include "Adafruit_Sensor.h"
#include "Adafruit_AM2320.h"
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
Adafruit_AM2320 am2320 = Adafruit_AM2320();


void setup() {
  String apiuser;
  String apipassword;
  Serial.begin(9600);
  am2320.begin();
  WiFi.begin("SSID", "PASS"); 
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("Waiting to connect…");
    }
  }

void loop() {
  float tempreading;
  float humidity;
  tempreading = am2320.readTemperature();
  humidity = am2320.readHumidity();
  HTTPClient http;
  DynamicJsonDocument doc(2048);
  String json;
  doc["temperature"] = tempreading;
  doc["timestamp"] = 0;
  doc["humidity"] = humidity;
  serializeJson(doc, json);

  http.begin("https://endpoint/records");
  http.addHeader("Content-Type", "application/json");
  http.setUserAgent("THERMO1");
  http.setAuthorization("username", "password");
  http.end();
  delay(1000); 
}





