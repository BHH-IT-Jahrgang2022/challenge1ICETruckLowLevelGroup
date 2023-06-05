#include <Arduino.h>
//#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClient.h>

//#include "mqttHandler.h"
#include "datahelper.h"

// sensor libs
#include "DHT.h"

// servo libs
#include <Servo.h>

int dhtSense = 23;

int statLED = 2;
int sendLED = 4;
int senseLED = 15;


WiFiClient wifiClient;
PubSubClient pubSubClient;

DataHelper datahelper;

/*
// change depending on sensor
String clientid = "ESP32Sense1";
String topicAlive = "/sensors/alive/ESP/";
String topicData = "/sensors/data/ESP/";
String topicControl = "/sensors/control/ESP/";
*/

/*
String clientid = "ESP32Fan1";
String topicAlive = "fans/ESP32Fan1/alive/";
String topicData = "fans/ESP32Fan1/data/";
String topicControl = "fans/ESP32Fan1/control/";
*/

String clientid = "ESP32Motors1";
String topicAlive = "motors/ESP32Motors1/alive/";
String topicData = "motors/ESP32Motors1/data/";
String topicFanControl = "motors/ESP32Motors1/fan/control/";
String topicServoControl = "motors/ESP32Motors1/servo/control/";

const char* domain = "pi-johanna.local";
const char* usernameMQTT = "low_level";
const char* passwordMQTT = "mqttguys";

const int freq = 5000;
const int ledChannel = 0;
const int resolution = 8;

const float targetTemp = -18.0;
const float maxDiff = 13.0;

DHT dht(dhtSense, DHT22);

Servo servoVent;
int servoPin = 21;

int fanPin = 19;

int oldPos = 15;

bool isSensor = false; // change mode from sensor to motor
bool isServo = false;
bool isFan = false; // change to fan mode
bool isCombi = true; //set to combi-mode: one ESP, servo and fan

void setLEDC(int brightness) {
    if (brightness >= 0 && brightness <= 255) {
        ledcWrite(ledChannel, brightness);
    }
    else if (brightness > 255) {
        ledcWrite(ledChannel, 255);
    }
    else if (brightness < 0) {
        ledcWrite(ledChannel, 0);
    }
    else {
        Serial.print("ERROR: LEDC brightness is not an int");
    }
}

void setFanC(int speed) {
    if (speed >= 0 && speed <= 255) {
        ledcWrite(ledChannel, speed);
    }
    else if (speed > 255) {
        ledcWrite(ledChannel, 255);
    }
    else if (speed < 0) {
        ledcWrite(ledChannel, 0);
    }
    else {
        Serial.print("ERROR: LEDC brightness is not an int");
    }
}

void setServoPos(int position) {
    if (position != oldPos) {
        int degr = 0;
        switch(position) {
            case 0:
                degr = 0;
                break;
            case 1:
                degr = 10;
                break;
            case 2:
                degr = 20;
                break;
            case 3:
                degr = 30;
                break;
            case 4:
                degr = 40;
                break;
            case 5:
                degr = 50;
                break;
            case 6:
                degr = 60;
                break;
            case 7:
                degr = 70;
                break;
            case 8:
                degr = 80;
                break;
            default:
                degr = 180;
                break;
        }
        servoVent.write(degr);
        oldPos = position;
    }
}

void callbackCombi(char* topic, byte *payload, unsigned int length) {
    payload[length] = 0;
    int value = String((char *) payload).toInt();
    if (strcmp(topic, topicFanControl.c_str())) {
        Serial.print(topic);
        Serial.println(value);
        setFanC(value);
    } else if (strcmp(topic, topicServoControl.c_str())) {
        Serial.print(topic);
        Serial.println(value);
        setServoPos(value);
    } else {
        Serial.println("ERROR: problem in combiCallback");
    }
}

void callback(char* topic, byte *payload, unsigned int length) {

    // this all is pfusch ==> TODO: Make it properly!
    payload[length] = 0;
    int step = String((char *) payload).toInt();
    Serial.print("topic: ");
    Serial.println(topic);
    Serial.print("data: ");
    Serial.write(payload, length);
    Serial.println();
}

void callbackServo(char* topic, byte *payload, unsigned int length) {

    // this all is pfusch ==> TODO: Make it properly!
    payload[length] = 0;
    int step = String((char *) payload).toInt();

    Serial.println(step);
    setServoPos(step);
}

void callbackFan(char* topic, byte *payload, unsigned int length) {

    // this all is pfusch ==> TODO: Make it properly!
    payload[length] = 0;
    int speed = String((char *) payload).toInt();

    Serial.println(speed);
    setFanC(speed);
}

void initMQTT() {

    pubSubClient = PubSubClient(wifiClient);

    pubSubClient.setServer(domain, 1883);
    /*
    if (isServo) {
        pubSubClient.setCallback(callbackServo);
    } else if (isFan) {
        pubSubClient.setCallback(callbackFan);
    } else {
        pubSubClient.setCallback(callback);
    }
    */

   pubSubClient.setCallback(callbackCombi);  // insert callback function according to ESP type

    while(!pubSubClient.connected()) {
        Serial.println("Attempting connection...");

        if (pubSubClient.connect(clientid.c_str(), usernameMQTT, passwordMQTT)) {
            Serial.println("MQTT connected");
            pubSubClient.publish(topicAlive.c_str(), "connect");
            pubSubClient.subscribe(topicFanControl.c_str());  // adjust control topic/s here (for now)
            pubSubClient.subscribe(topicServoControl.c_str());
        } else {
            Serial.print("Failed, trying again! REASON: ");
            Serial.print(pubSubClient.state());
            Serial.println("");
            delay(10000);
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
  
    WiFi.begin("BembelNet", "Go2TheBembelWifiNetwork2023!");

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

void initServo() {
    servoVent.attach(servoPin);
    servoVent.write(0); // home it
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

void setPinStatusServo() {
    Serial.println("Setting status LED...");
    pinMode(statLED, OUTPUT);

    Serial.println("Setting data LED...");
    pinMode(sendLED, OUTPUT);

    Serial.println("Setting sensor LED...");
    pinMode(senseLED, OUTPUT);

    Serial.println("Setting dht sensor pin...");
    pinMode(dhtSense, INPUT);

    pinMode(servoPin, OUTPUT);
}

void LEDCSetup(int ledPin) {
    ledcSetup(ledChannel, freq, resolution);
    ledcAttachPin(ledPin, ledChannel);
}

void fanCSetup(int fanPin) {
    ledcSetup(ledChannel, freq, resolution);
    ledcAttachPin(fanPin, ledChannel);
}

int tempBrightness(float temp) {
    if (temp == -18.0) {
        return 0;
    }
    else {
        float diff = targetTemp - temp;
        if (diff > 0) {
            float brightness = diff * 255 / maxDiff;
            int brightnessInt =static_cast<int>(brightness);
            return brightnessInt;
        }
        else {
            diff = -diff;
            float brightness = diff * 255 / maxDiff;
            int brightnessInt =static_cast<int>(brightness);
            return brightnessInt;
        }

    }
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

void initSensorPart() {
    // Pin init
    Serial.println("==== Initializing pins                      ====");

    setPinStatus();

    Serial.println("==== Initialized pins                       ====");

    Serial.println("==== Initializing DHT Sensor                ====");

    initDHT();

    Serial.println("==== Initialized DHT Sensor                 ====");
}

void initServoPart() {
    Serial.println("==== Initializing pins                      ====");

    setPinStatusServo();

    Serial.println("==== Initialized pins                       ====");

    Serial.println("==== Initializing servo                     ====");

    initServo();

    Serial.println("==== Initialized servo                      ====");
}

void initFanPart() {
    Serial.println("==== Initializing pins                      ====");

    fanCSetup(fanPin);

    Serial.println("==== Initialized pins                       ====");

    setFanC(0);
}

void initCombi() {
    initServoPart();
    initFanPart();
}

void setup() {
    
    Serial.begin(115200);
    Serial.println("================================================");
    Serial.println("==== ESP32; challenge1ICETruck Arduino Code ====");
    Serial.println("==== Compiled on 30/05/2023                 ====");
    Serial.println("==== Booting up                             ====");

/*
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
*/

    if (isSensor) {
        initSensorPart();
    } else if (isFan) {
        initFanPart();
    } else if (isServo) {
        initServoPart();
    } else if (isCombi) {
        initCombi();
    } else {
        Serial.println("!!#!!     no ESP type given    !!#!!");
        while(true) {

        }
    }

    Serial.println("==== Initializing WiFi ====");

    // Init WiFi
    initWiFi();

    Serial.println("==== Initialized WiFi ====");

    Serial.println("Waiting 10 seconds for connections to clean up...");

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
    //LEDCSetup(senseLED);
}

void loop() {

    if (isSensor) {
        publishTempReading(getTempReading());
        delay(1000);
    } else {
        pubSubClient.loop();
    }
/*
    for (int i = 0; i <= 255; i++) {
        setLEDC(i);
        delay(50);
    }
    Serial.println("==== Brightness of LED highest ===");

    for (int i = 255; i >= 0; i--) {
        setLEDC(i);
        delay(50);
    }
    Serial.println("=== Brightness of LED low ===");
    publishTempReading(getTempReading());
    delay(1000);
*/
}