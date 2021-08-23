#include "Adafruit_Sensor.h"
#include "Adafruit_AM2320.h"
#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
Adafruit_AM2320 am2320 = Adafruit_AM2320();

void setup() {
  //DEFINE VARIABLES AND OPEN WIFI CONNECTION
  String apiuser;
  String apipassword;
  Serial.begin(9600);
  am2320.begin();
  WiFi.begin("XXXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXX"); 
  while (WiFi.status() != WL_CONNECTED) {  
      delay(500);
      Serial.println("Connecting…");
  }
  Serial.println("WIFI ok");
  }

void loop() {

  float heatenings;
  float humidity;
  heatenings = am2320.readTemperature();
  humidity = am2320.readHumidity();
  HTTPClient http;
  DynamicJsonDocument doc(2048);
  String json;
  doc["temperature"] = heatenings;
  doc["timestamp"] = 0;
  doc["humidity"] = humidity;
  serializeJson(doc, json);
  unsigned long seconds = 1000L;
  unsigned long minutes = seconds * 60;
  delay(minutes);
  http.begin("https://XXXXXXXXXXX/api/records");
  http.addHeader("Content-Type", "application/json");
  //SET IDENTITY FOR SENSOR
  http.setUserAgent("THERMO1");
  http.setAuthorization("XXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXX");
  int httpCode = http.POST(json);
  http.end(); 
}