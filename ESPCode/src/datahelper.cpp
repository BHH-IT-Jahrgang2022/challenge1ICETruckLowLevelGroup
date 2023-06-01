#include "datahelper.h"

DataHelper::DataHelper() {
    
    if (initFS() == 0) {
    Serial.println("Initalized FS");
  } else {
    Serial.println("Error occured initializing, abording startup");
    return;
  }

  if (loadDotEnv() == 0) {
    Serial.println("Loaded environment file");
  } else {
    Serial.println("Error loading environment files, aborting");
    return;
  }
}

int DataHelper::initFS() {
    if(!SPIFFS.begin(true)) {
        Serial.println("ERROR: ABORT. COULD NOT OPEN SPIFFS");
        return -1;
    }
    return 0;
}

int DataHelper::loadDotEnv() {
   File file = SPIFFS.open("/.env");
   //File file = SPIFFS.open("/test.txt");

    if(!file) {
        Serial.println("ERROR: ABORT MISSION. COULD NOT LOAD FILE");
        return -1;
    }

    // printing out the file (later will be handled by .env encoder)
    std::list<std::string> rawData;
    Serial.println("The file content");
    while (file.available()) {
        String curr = file.readStringUntil('\n');
        Serial.print(curr);
        Serial.println();
        rawData.push_back(curr.c_str()); // conv to cpp string and add it to the list
    }
    file.close();
    Serial.println("");
    dotEnvContent = parseDotEnvToMap(rawData); // convert it 
    if (dotEnvContent.size() == 0) { // it can not be empty, so if it is, error out
        return -1;
    }
    Serial.println(dotEnvContent.at("ssid").c_str());
    Serial.println("SUCCESS");
    return 0;
}

std::map<std::string, std::string> DataHelper::parseDotEnvToMap(std::list<std::string> rawData) {
    Serial.println(rawData.size()); // outputs 2
    std::map<std::string, std::string> data;
    for (std::string currLine : rawData) {
        std::string key = currLine.substr(0, currLine.find("="));
        Serial.print(key.c_str()); // print out value for eval
        Serial.print(": ");
        std::string value = currLine.substr(currLine.find("=") + 1);
        Serial.println(value.c_str());
        data.insert({key, value});

    }
    return data;
}

std::array<std::string, 2> DataHelper::getWiFiCredentials() {
    std::string ssid = dotEnvContent.at("ssid");
    std::string pass = dotEnvContent.at("pass");
    return {ssid, pass};
}

std::string DataHelper::getWiFiSSID() {
    return dotEnvContent.at("ssid");
}

std::string DataHelper::getWiFiPASSWD() {
    return dotEnvContent.at("pass");
}
