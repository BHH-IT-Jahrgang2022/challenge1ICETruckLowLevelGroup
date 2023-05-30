#include "string";

class MQTTHandler {
public:
    MQTTHandler();
    int authorize(std::string domain, std::string username, std::string password);
    void sendMessage();
    void sendAlive();
    bool connected();

private:
    std::string serverDomain;
    std::string username;
    std::string password;

};