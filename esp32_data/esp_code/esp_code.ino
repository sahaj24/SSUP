#include <WiFi.h>
#include <ArduinoJson.h>
#include <ESPAsyncWebServer.h>

// WiFi credentials
const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

AsyncWebServer server(80);

float generateRandomValue(float min, float max) {
  return random(min * 100, max * 100) / 100.0;  // Returns a value between min and max
}

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    StaticJsonDocument<200> doc;

    doc["timestamp"] = millis();  // Use millis() as a timestamp
    doc["temperature"] = generateRandomValue(20.0, 40.0);  // Random temperature between 20°C and 40°C
    doc["humidity"] = generateRandomValue(30.0, 70.0);      // Random humidity between 30% and 70%
    doc["gasLevel"] = generateRandomValue(0.0, 500.0);      // Random gas level between 0 ppm and 500 ppm
    doc["pressure"] = generateRandomValue(90000.0, 110000.0); // Random pressure between 90,000 Pa and 110,000 Pa

    String jsonData;
    serializeJson(doc, jsonData);
    request->send(200, "application/json", jsonData);  // Return data as JSON
  });

  server.begin();
}

void loop() {
}
