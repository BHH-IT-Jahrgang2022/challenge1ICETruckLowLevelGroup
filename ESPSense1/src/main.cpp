#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClient.h>

// sensor libs
#include "DHT.h"

// servo libs
#include <Servo.h>


// connection and mqtt
WiFiClient wifiClient;
PubSubClient pubSubClient;


// LEDs
int statLED = 2;
int sendLED = 4;
int senseLED = 15;

// sensor
int dhtSense = 23;




// change depending on sensor
String clientid = "ESP32Sense1";
String topicAlive = "sensors/ESP32Sense1/alive/";
String topicData = "sensors/ESP32Sense1/temp/data/";
String topicControl = "sensors/control/";



// more global configs
const char* domain = "pi-johanna.local";
const char* usernameMQTT = "low_level";
const char* passwordMQTT = "mqttguys";

const int freq = 5000;
const int ledChannel = 0;
const int resolution = 8;

const int fanChannel = 8;

float targetTemp = -18.0;
const float maxDiff = 7.0;

DHT dht(dhtSense, DHT22);

Servo servoVent;
int servoPin = 19;

int fanPin = 32;

int oldPos = 15;

bool isSensor = true; // change mode from sensor to motor
bool isServo = false;
bool isFan = false; // change to fan mode
bool isCombi = false; //set to combi-mode: one ESP, servo and fan


// functions to setup and use the esp connected motors and sensors

// turn white led on for a short time (flash)
void flash() {
    digitalWrite(sendLED, HIGH);
    delay(200);
    digitalWrite(sendLED, LOW);
}

// set LEDC value, brightness is variable
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

// set FanC value, speed is variable
void setFanC(int speed) {
    if (speed >= 0 && speed <= 255) {
        ledcWrite(fanChannel, speed);
    }
    else if (speed > 255) {
        ledcWrite(fanChannel, 255);
    }
    else if (speed < 0) {
        ledcWrite(fanChannel, 0);
    }
    else {
        Serial.print("ERROR: FanC speed is not an int");
    }
}

// set servo position, value 0 to 8
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

// merged callback function for fan and servo
void callbackCombi(char* topic, byte *payload, unsigned int length) {
    payload[length] = 0;
    String topicString = topic;
    int value = String((char *) payload).toInt();
    if (topicString.equals(topicControl)) {
        Serial.print(topic);
        Serial.println(value);
        setFanC(value);
    } else if (topicString.equals(topicControl)) {
        Serial.print(topic);
        Serial.println(value);
        setServoPos(value);
    } else {
        Serial.println("ERROR: problem in combiCallback");
    }
    flash();
}

// clabback function for sensors
void callback(char* topic, byte *payload, unsigned int length) {

    // this all is pfusch ==> TODO: Make it properly!
    payload[length] = 0;
    int step = String((char *) payload).toInt();
    Serial.print("topic: ");
    Serial.println(topic);
    Serial.print("data: ");
    Serial.write(payload, length);
    Serial.println();
    flash();
}

// callback function for servo
void callbackServo(char* topic, byte *payload, unsigned int length) {

    // this all is pfusch ==> TODO: Make it properly!
    payload[length] = 0;
    int step = String((char *) payload).toInt();

    Serial.println(step);
    setServoPos(step);
    flash();
}

// callback function for fan
void callbackFan(char* topic, byte *payload, unsigned int length) {

    // this all is pfusch ==> TODO: Make it properly!
    payload[length] = 0;
    int speed = String((char *) payload).toInt();

    Serial.println(speed);
    setFanC(speed);
    flash();
}

// initialize mqtt
void initMQTT() {

    pubSubClient = PubSubClient(wifiClient);

    pubSubClient.setServer(domain, 1883);

   pubSubClient.setCallback(callback);  // insert callback function according to ESP type

    while(!pubSubClient.connected()) {
        Serial.println("Attempting connection...");

        if (pubSubClient.connect(clientid.c_str(), usernameMQTT, passwordMQTT)) {
            Serial.println("MQTT connected");
            pubSubClient.publish(topicAlive.c_str(), "connect");
            pubSubClient.subscribe(topicControl.c_str());  // adjust control topic/s here (for now)
        } else {
            Serial.print("Failed, trying again! REASON: ");
            Serial.print(pubSubClient.state());
            Serial.println("");
            delay(10000);
        }
    }
}

// initialize wifi
void initWiFi() {
    Serial.println("Initializing SPFISS...");

    Serial.println("Connecting to WiFi...");

    Serial.println("Loading credentials...");

    Serial.println("Connecting");
  
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

// initialize temp sensor
void initDHT() {
    dht.begin();
}

// initialize servo motor
void initServo() {
    servoVent.attach(servoPin);
    servoVent.write(0); // home it
}

// set status led to on
void turnStatLEDOn() {
    digitalWrite(statLED, HIGH);
}

// setup LED for LEDC
void LEDCSetup(int ledPin) {
    ledcSetup(ledChannel, freq, resolution);
    ledcAttachPin(ledPin, ledChannel);
}

// setup pin outputs for sensor esps
void setPinStatus() {
    Serial.println("Setting status LED...");
    pinMode(statLED, OUTPUT);

    Serial.println("Setting data LED...");
    pinMode(sendLED, OUTPUT);

    Serial.println("Setting sensor LED...");
    pinMode(senseLED, OUTPUT);
    LEDCSetup(senseLED);
    setLEDC(0);

    Serial.println("Setting dht sensor pin...");
    pinMode(dhtSense, INPUT);
}

// setup pin outputs for motors esps
void setPinStatusMotors() {
    Serial.println("Setting status LED...");
    pinMode(statLED, OUTPUT);

    Serial.println("Setting data LED...");
    pinMode(sendLED, OUTPUT);
}

// setup fan pin for LEDC
void fanCSetup(int fanPin) {
    ledcSetup(fanChannel, freq, resolution);
    ledcAttachPin(fanPin, fanChannel);
}

// convert temperature to brightness of temp led (for LEDC)
int tempBrightness(float temp) {
    if (temp == targetTemp) {
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

// read out current temperature
float getTempReading() {
    float temp = dht.readTemperature();
    Serial.print("Temp: ");
    Serial.print(temp);
    Serial.println("°C");
    return temp;
}

// publish temp to mqtt
void publishTempReading(float temp) {
    Serial.println("#*#*#");
    Serial.println(temp);
    std::string tempString = std::to_string(temp);
    Serial.println(tempString.c_str());
    Serial.println("#*#*#");
    pubSubClient.publish(topicData.c_str(), tempString.c_str());
    flash();
}

// initialize esp as sensor esp
void initSensorPart() {
    // Pin init
    Serial.println("==== Initializing pins                      ====");

    setPinStatus();

    Serial.println("==== Initialized pins                       ====");

    Serial.println("==== Initializing DHT Sensor                ====");

    initDHT();

    Serial.println("==== Initialized DHT Sensor                 ====");
}

// initialize esp to servo usage
void initServoPart() {
    Serial.println("==== Initializing servo                     ====");

    pinMode(servoPin, OUTPUT);
    initServo();

    Serial.println("==== Initialized servo                      ====");
}

// initialize esp to fan usage
void initFanPart() {
    Serial.println("==== Initializing pins                      ====");

    fanCSetup(fanPin);

    Serial.println("==== Initialized pins                       ====");

    setFanC(0);
}

// initialize esp for combi motors usage (fan and servo)
void initCombi() {
    Serial.println("==== Initializing pins                      ====");

    setPinStatusMotors();

    Serial.println("==== Initialized pins                       ====");
    initServoPart();
    initFanPart();
}


void setup() {
    
    Serial.begin(115200);
    Serial.println("================================================");
    Serial.println("==== ESP32; challenge1ICETruck Arduino Code ====");
    Serial.println("==== Compiled on 09/06/2023                 ====");
    Serial.println("==== Booting up                             ====");

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
    flash();
    Serial.println("================================================");
    
    turnStatLEDOn();
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

/*
    setFanC(0);
    setServoPos(0);
    Serial.println();
    Serial.println("+++   +++   Motors set to 0   +++   +++");
    delay(1000);
    setServoPos(2);
    Serial.println("+++   +++   Servo set to position 2   +++   +++");
    delay(1000);
    setFanC(160);
    Serial.println("+++   +++   Fan set to 160   +++   +++");
    delay(1000);
    setServoPos(6);
    Serial.println("+++   +++   Servo set to position 6   +++   +++");
    delay(1000);
    setFanC(255);
    Serial.println("+++   +++   Fan set to 255   +++   +++");
    delay(1000);
    setServoPos(0);
    Serial.println("+++   +++   Servo set to position 0   +++   +++");
    delay(1000);
    setFanC(100);
    Serial.println("+++   +++   Fan set to 100   +++   +++");
    delay(1000);
    setServoPos(8);
    Serial.println("+++   +++   Servo set to position 8   +++   +++");
    delay(1000);
    setFanC(0);
    Serial.println("+++   +++   Fan set to 0   +++   +++");
    delay(1000);
*/
}