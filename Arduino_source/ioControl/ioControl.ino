#include <Wire.h>
#define I2C_ADDR 0x08

#include "Adafruit_NeoPixel.h"
#include "ledColor.h" // "WS2812_Definitions.h"

#define LED_PIN 4
#define LED_COUNT 4
Adafruit_NeoPixel LEDs =
    Adafruit_NeoPixel(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

String responceMessage="";
unsigned long viewColor = 0;
unsigned long viewTime  = 0;
unsigned long viewInterval = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("IO control start...");

  Wire.begin(I2C_ADDR);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

  LEDs.begin();
  clearLEDs();
  LEDs.show();

  viewTime = 0;
}

void loop() {
  if( (millis()-viewTime) < viewInterval ) {
    //showLEDs(viewColor, TOP_DOWN, 50);
    //showLEDs(viewColor, DOWN_TOP, 50);
    showLEDs(viewColor, ALL, 50);
  } else {
    clearLEDs();
  }
}

void requestEvent(int howmany){
  Wire.write(responceMessage.c_str());
}

void receiveEvent(int howmany){
  char txt[32] = "";
  int seq = 0;

  while(Wire.available()){
    char c = Wire.read();
    txt[seq++] = c;
    delay(10);
  }
  txt[seq] = '\0';
  responceMessage = "ok";

  String str = String(txt);
  Serial.print("ReceiveData:[");
  Serial.print(str.length()); Serial.print("][");
  Serial.print(str); Serial.println("]");

  if(str == "0") {
    viewColor = GREEN;
  } else if(str == "1") {
    viewColor = RED;
  } else if(str == "2") {
    viewColor = BLACK; //WHITE;
  }
  viewTime = millis();
  viewInterval = 10000;
}

void showLEDs(unsigned long color, byte direction, byte wait){
  if (direction == TOP_DOWN) {
    for (int i=0; i<LED_COUNT; i++) {
      clearLEDs();  // Turn off all LEDs
      LEDs.setPixelColor(i, color);
      LEDs.show();
      delay(wait);
    }
  } else if (direction == DOWN_TOP) {
    for (int i=LED_COUNT-1; i>=0; i--) {
      clearLEDs();
      LEDs.setPixelColor(i, color);
      LEDs.show();
      delay(wait);
    }
  } else if (direction == ALL) {
    for (int i=0; i<LED_COUNT; i++) {
      LEDs.setPixelColor(i, color);
    }
    LEDs.show();
    delay(wait);
  }
}

void clearLEDs() {
  for(int i=0; i<LED_COUNT; i++) {
    LEDs.setPixelColor(i, 0);
  }
  LEDs.show();
}
