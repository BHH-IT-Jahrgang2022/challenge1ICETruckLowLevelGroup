#include <Arduino.h>
#include <array>
#include <SPIFFS.h>
#include <map>
#include <list>
#include <iterator>

class DataHelper {
public:
    DataHelper();
    std::array<std::string, 2> getWiFiCredentials();
    std::string getDotEnvFile();
    std::string getWiFiSSID();
    std::string getWiFiPASSWD();
private:
    std::map<std::string, std::string> dotEnvContent;
    std::map<std::string, std::string> parseDotEnvToMap(std::list<std::string> rawData);
    int loadDotEnv();
    int initFS();
};