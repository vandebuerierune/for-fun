#include <ArduinoIoTCloud.h>
#include <WiFi.h>
/* should not be necesarry as these are parsed through the cloud portal.
const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";
*/
#define RED_PIN     5
#define GREEN_PIN   18
#define BLUE_PIN    19

int brightness;
String color;
String pattern;

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  WiFi.begin(SECRET_SSID, SECRET_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize Arduino Cloud with the secret key
  ArduinoCloud.begin(ArduinoIoTPreferredConnection, SECRET_KEY);
  
  ArduinoCloud.addProperty(brightness, READWRITE, ON_CHANGE, onBrightnessChange);
  ArduinoCloud.addProperty(color, READWRITE, ON_CHANGE, onColorChange);
  ArduinoCloud.addProperty(pattern, READWRITE, ON_CHANGE, onPatternChange);
}

void loop() {
  ArduinoCloud.update();
}

void onBrightnessChange() {
  updateColor();
}

void onColorChange() {
  updateColor();
}

void onPatternChange() {
  if (pattern == "breathing") {
    breathingEffect();
  } else if (pattern == "party") {
    partyEffect();
  } else if (pattern == "christmas") {
    christmasEffect();
  } else {
    updateColor(); // Default to static color
  }
}

void updateColor() {
  long number = strtol(&color[1], NULL, 16);
  int r = (number >> 16) & 0xFF;
  int g = (number >> 8) & 0xFF;
  int b = number & 0xFF;
  analogWrite(RED_PIN, r * brightness / 255);
  analogWrite(GREEN_PIN, g * brightness / 255);
  analogWrite(BLUE_PIN, b * brightness / 255);
}

// effects
void breathingEffect() {
  static uint8_t brightness = 0;
  static int8_t direction = 1;
  
  brightness += direction;
  if (brightness == 0 || brightness == 255) {
    direction = -direction;
  }
  
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Orange; // Change to your desired color
    leds[i].fadeLightBy(255 - brightness);
  }
  FastLED.show();
  delay(10); // Adjust for speed of breathing
}

void partyEffect() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(random(0, 255), 255, 255);
  }
  FastLED.show();
  delay(100); // Adjust for speed of color change
}

void christmasEffect() {
  for (int i = 0; i < NUM_LEDS; i++) {
    if (i % 2 == 0) {
      leds[i] = CRGB::Red;
    } else {
      leds[i] = CRGB::Green;
    }
  }
  FastLED.show();
  delay(500); // Adjust for speed of color change
}