#include <Arduino.h>
//#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClient.h>

//#include "mqttHandler.h"
#include "datahelper.h"

// sensor libs
#include "DHT.h"

int dhtSense = 23;

int statLED = 2;
int sendLED = 4;
int senseLED = 15;


WiFiClient wifiClient;
PubSubClient pubSubClient;

DataHelper datahelper;

String clientid = "ESP32Sense1";
String topicAlive = "/sensors/alive/ESP/";
String topicData = "/sensors/data/ESP/";
String topicControl = "/sensors/control/ESP/";

const char* domain = "pi-johanna.local";
const char* usernameMQTT = "low_level";
const char* passwordMQTT = "mqttguys";

DHT dht(dhtSense, DHT22);

void callback(char* topic, byte *payload, unsigned int length) {
    Serial.println("------------new message from broker----------");
    Serial.print("channel: ");
    Serial.println(topic);
    Serial.print("data: ");
    Serial.write(payload, length);
    Serial.println();
}

void initMQTT() {

    pubSubClient = PubSubClient(wifiClient);

    pubSubClient.setServer(domain, 1883);
    pubSubClient.setCallback(callback);

    while(!pubSubClient.connected()) {
        Serial.println("Attempting connection...");

        if (pubSubClient.connect(clientid.c_str(), usernameMQTT, passwordMQTT)) {
            Serial.println("MQTT connected");
            pubSubClient.publish(topicAlive.c_str(), "connect");
            pubSubClient.subscribe(topicControl.c_str());
        } else {
            Serial.print("Failed, trying again! REASON: ");
            Serial.print(pubSubClient.state());
            Serial.println("");
            delay(2000);
        }
    }
}

void initWiFi() {
    Serial.println("Initializing SPFISS...");

    datahelper = DataHelper();

    Serial.println("Connecting to WiFi...");

    Serial.println("Loading credentials...");

    std::array<std::string, 2> credentials = datahelper.getWiFiCredentials();

    Serial.println("Connecting");
    // TODO: Debug Wifi shit

    Serial.println("*#*#*");
    Serial.println(datahelper.getWiFiSSID().c_str());
    Serial.println(datahelper.getWiFiPASSWD().c_str());
    Serial.println("*#*#*");

    //WiFi.begin(datahelper.getWiFiSSID().c_str(), datahelper.getWiFiPASSWD().c_str());
  
    WiFi.begin("TEST", "TETS");

    while(WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println(WiFi.status());
    }
    Serial.println("");

    Serial.println("Connected");

    Serial.print("Your IP is: ");

    Serial.println(WiFi.localIP().toString());
}

void initDHT() {
    dht.begin();
}

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

float getTempReading() {
    float temp = dht.readTemperature();
    Serial.print("Temp: ");
    Serial.print(temp);
    Serial.println("°C");
    return temp;
}

void publishTempReading(float temp) {
    Serial.println("#*#*#");
    Serial.println(temp);
    std::string tempString = std::to_string(temp);
    Serial.println(tempString.c_str());
    Serial.println("#*#*#");
    pubSubClient.publish(topicData.c_str(), tempString.c_str());
}

void setup() {
    Serial.begin(115200);
    Serial.println("================================================");
    Serial.println("==== ESP32; challenge1ICETruck Arduino Code ====");
    Serial.println("==== Compiled on 30/05/2023                 ====");
    Serial.println("==== Booting up                             ====");

    // Pin init

    Serial.println("==== Initializing pins                      ====");

    setPinStatus();

    Serial.println("==== Initialized pins                       ====");

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
    Serial.println("==== Initializing DHT Sensor ====");

    initDHT();

    Serial.println("==== Initialized DHT Sensor ====");

    Serial.println("==== Initializing WiFi ====");

    // Init WiFi
    initWiFi();

    Serial.println("==== Initialized WiFi ====");

    Serial.println("Waiting 5 seconds for connections to clean up...");

    delay(10000);

    // Init MQTT

    Serial.println("==== Initializing MQTT                      ====");
        
    initMQTT();

    Serial.println("==== Initialized MQTT                       ====");


    // End sequence (cleaning up the rest)
    Serial.println("====          Finished starting up          ====");
    Serial.println("====          Starting main process         ====");
    Serial.println("==== Communication alive to MQTT ====");
    pubSubClient.publish(topicAlive.c_str(), "alive");
    //mqttHandler.sendAlive();
    Serial.println("================================================");
    
    turnStatLEDOn();

}

void loop() {
    publishTempReading(getTempReading());
    delay(1000);
}