
#include <Wire.h>
#define I2C_ADDR 0x08
#define SCL_PIN  15  // GPIO15  // SDA_PIN 데이터선 // 나노기준 A5
#define SDA_PIN  14  // GPIO14  // SCL_PIN 클럭선  // 나노기준 A4   

//TwoWire i2c = TwoWire(0);



void i2c_send(String msg) {
    Wire.begin(SDA_PIN, SCL_PIN);
    Wire.beginTransmission(I2C_ADDR); // transmit to device #8
    Wire.write(msg.c_str());
    byte res = Wire.endTransmission(); // stop transmitting delay(100);

    Serial.print(",\t request:'");
    Serial.print(msg);
    Serial.print("', status:'");
    Serial.print(res);
    Serial.print("'");

    delay(100);
    Wire.requestFrom(I2C_ADDR, 2);

    Serial.print(", responce:'");
    while(Wire.available()){
      char c = Wire.read();
      Serial.print(c);
    }

    Serial.println("'");
}
