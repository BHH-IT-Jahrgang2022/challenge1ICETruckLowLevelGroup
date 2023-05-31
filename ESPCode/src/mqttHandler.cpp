#include "mqttHandler.h"
#include "PubSubClient.h"

MQTTHandler::MQTTHandler() {
}

int MQTTHandler::authorize(std::string domain, std::string username, std::string password) {
    if (username.empty() | username == " ") {
        // crash if username is empty
        return -1;
    } 

    return 0;
}

void MQTTHandler::sendAlive() {
    // TODO: Add code to send alive message
}