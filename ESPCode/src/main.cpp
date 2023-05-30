#include <arduino.h>
#include <Wire.h>

#include "mqttHandler.h"

int dhtSense = 21;

int statLED = 2;
int sendLED = 4;
int senseLED = 15;

MQTTHandler mqttHandler;

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
    Serial.begin(115200);
    Serial.println("================================================");
    Serial.println("==== ESP32; challenge1ICETruck Arduino Code ====");
    Serial.println("==== Compiled on 30/05/2023 ====");
    Serial.println("==== Booting up ====");

    // Pin init

    Serial.println("==== Initializing pins ====");

    setPinStatus();

    Serial.println("==== Initialized pins ====");

    // I2C Init
/*
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
*/
    // Init MQTT

    Serial.println("==== Initializing MQTT ====");
        
    Serial.println("Login you in...");
    int resp = mqttHandler.authorize("domain", "username", "password");
    if (resp == -1) {
        Serial.println("Login failed! Aborting!");
        return;
    } else {
        Serial.println("Login successfull");
    }
    Serial.println("Sending alive message");
    mqttHandler.sendAlive();
    Serial.println("==== Initialized MQTT ====");


    // End sequence
    Serial.println("==== Finished starting up ====");
    Serial.println("==== Starting main process ====");

    Serial.println("================================================");

}

void loop() {
    // read out temp
    digitalWrite(statLED, HIGH);
    digitalWrite(sendLED, HIGH);
    digitalWrite(senseLED, HIGH);
    delay(500);
    digitalWrite(statLED, LOW);
    digitalWrite(sendLED, LOW);
    digitalWrite(senseLED, LOW);
    delay(500);
}