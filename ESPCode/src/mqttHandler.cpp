#include "mqttHandler.h"
#include "arduino.h"

MQTTHandler::MQTTHandler() {
    Serial.println("HUHU");
    //WiFiClient wifiClient;
    Serial.println("HEHE");
    pubSubClient = PubSubClient();
    Serial.println("HIHI");
}

int MQTTHandler::authorize(std::string domain, int port, std::string username, std::string password) {
    if (username.empty() | username == " ") {
        // crash if username is empty
        return -1;
    } 

    Serial.println("Before pubSubClient");

    std::string clientid = "ESP32Sense1";

    topicAlive = topicAlive + clientid + "/";
    topicData = topicData + clientid + "/";
    topicControl = topicControl + clientid + "/";

    Serial.println("Before while");
    while(!pubSubClient.connected()) {
        Serial.println("Attempting connection");
        

        // conn attempt
        if (pubSubClient.connect(clientid.c_str(), username.c_str(), password.c_str())) {
            Serial.println("MQTT connected");
            sendConnected();
            pubSubClient.subscribe(topicControl.c_str());
        } else {
            Serial.print("Failed, trying again");
            Serial.print(pubSubClient.state());
            Serial.println("");
            delay(2000);
        }
    }

    return 0;
}

void MQTTHandler::callback(char* topic, byte *payload, unsigned int length) {
    Serial.println("------------new message from broker----------");
    Serial.print("channel: ");
    Serial.println(topic);
    Serial.print("data: ");
    Serial.write(payload, length);
    Serial.println();
}

void MQTTHandler::sendConnected() {
    // TODO: Add code to send alive message
    pubSubClient.publish(topicAlive.c_str(), "connect");
}

void MQTTHandler::sendAlive() {
    pubSubClient.publish(topicAlive.c_str(), "alive");
}