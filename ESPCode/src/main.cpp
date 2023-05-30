#include <arduino.h>
#include <Wire.h>

int dhtSense = 11;
int i2cSDA = 23;
int i2cSCL = 24;

int statLED = 10;
int sendLED = 12;
int senseLED = 13;

void turnStatLEDOn() {
    digitalWrite(statLED, HIGH);
}

void setPinStatus() {
    Serial.println("Setting status LED...");
    pinMode(statLED, OUTPUT);

    Serial.println("Setting data LED...");
    pinMode(sendLED, OUTPUT);

    Serial.println("Setting sensor LED...");
    pinMode(senseLED, OUTPUT);

    Serial.println("Setting dht sensor pin...");
    pinMode(dhtSense, INPUT);
}

void setup() {
    Serial.begin(9600);
    Serial.println("================================================");
    Serial.println("==== ESP32; challenge1ICETruck Arduino Code ====");
    Serial.println("==== Compiled on 30/05/2023 ====");
    Serial.println("==== Booting up ====");

    // Pin init

    Serial.println("==== Initializing pins ====");

    setPinStatus();

    Serial.println("==== Initialized pins ====");


    // I2C Init

    Serial.println("==== Initializing I2C ===");
    
    Serial.println("Setting pins...");
    Wire.setPins(i2cSDA, i2cSCL);
    Serial.println("Enabling I2C...");
    
    bool status = Wire.begin();
    
    if (status) {
        turnStatLEDOn();
        Serial.println("Started I2C successfully...");
    } else {
        Serial.println("ERROR! Failed to init I2C! Aborting startup!");
        return;
    }
    
    Serial.println("==== Initialized I2C ====");

    // End sequence
    Serial.println("==== Finished starting up ====");
    Serial.println("==== Starting main process ====");

    Serial.println("================================================");

}

void loop() {
    // read out temp
}
