#include "string"
#include "PubSubClient.h"
#include "WiFiClient.h"

class MQTTHandler {
public:
    MQTTHandler();
    int authorize(std::string domain, int port, std::string username, std::string password);
    void sendMessage();
    void sendAlive();
    void sendConnected();
    bool connected();

    void callback(char* topic, byte *payload, unsigned int length);

private:
    PubSubClient pubSubClient;
    std::string topicAlive = "/sensors/alive/";
    std::string topicData = "/sensors/data/";
    std::string topicControl = "/sensors/control/";
    

};