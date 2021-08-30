#include "Adafruit_Sensor.h"
#include "Adafruit_AM2320.h"
#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
Adafruit_AM2320 am2320 = Adafruit_AM2320();
//WIFI SETTINGS
String wifiname = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
String wifipassword = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";

//UNIQUE DEVICE ID FOR LOGGING DATA
String uniquedeviceid = "THERMO1";

//YOUR GENERATED CREDENTIALS FOR THE FLASK APP
String apiusername = "XXXXXXXXXXXXXXXXXXXXXXXXXX";
String apipassword = "XXXXXXXXXXXXXXXXXXX";

//API END-POINT, SHOULD REFLECT APACHE2/OTHER HTTP SERVER CONFIG ROUTES
String apiendpoint = "https://XXXXXXXXXXXXXXXXXXXXXXXXX/api/records";


void setup() {
  Serial.begin(9600);
  am2320.begin();
  WiFi.begin(wifiname.c_str(), wifipassword.c_str()); 
  while (WiFi.status() != WL_CONNECTED) {  
      delay(500);
      Serial.println("Connecting…");
  }
  Serial.println("WIFI ok");
  }

void loop() {

  float tempreading;
  float humidity;
  tempreading = am2320.readTemperature();
  humidity = am2320.readHumidity();
  delay(1500);
  Serial.print("Humidity ");
  Serial.println(humidity);
  Serial.print("Temperature: ");
  Serial.println(tempreading);
  if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;
      DynamicJsonDocument doc(2048);
      String json;
      doc["temperature"] = tempreading;
      doc["timestamp"] = 0;
      doc["humidity"] = humidity;
      serializeJson(doc, json);
      unsigned long seconds = 1000L;
      unsigned long minutes = seconds * 60;
      
      http.begin(apiendpoint);
      http.addHeader("Content-Type", "application/json");
      //SET IDENTITY FOR SENSOR
      http.setUserAgent(uniquedeviceid);
      http.setAuthorization(apiusername.c_str(), apipassword.c_str());
      int httpCode = http.POST(json);
      http.end(); 
      delay(minutes);
  }
  else {
    Serial.println("Lost connection");
  }

}