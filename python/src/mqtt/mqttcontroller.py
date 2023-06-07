import mqttbroker as mqtt
import threading

class MQTTController:
    def start(self):
        self.running = True
        self.loop()
    
    def loop(self):
        while self.running:
            input = input("Commands: stop, connect, subscribe [topic], unsubscribe [topic]")
            if input == "stop":
                if self.broker.is_running():
                    message = "disconnected successfully"
                    try:
                        self.stop()
                    except Exception as e:
                        message = "Error on disconnect: " + str(e)
                    print(message)
            elif input == "connect":
                if self.broker.is_running():
                    print("MQTT-Broker is already running!")
                else:
                    message = "connected successfully"
                    try:
                        mqtt_thread = threading.Thread(target=self.broker.connect_mqtt)
                        mqtt_thread.start()
                    except Exception as e:
                        message = "Error on connect: " + str(e)
                    print(message)
            if input.__len__() > 10:
                if input[:9] == "subscribe":
                    if input[10] == "":
                        topic = input[:11]
                        if self.broker.is_running():
                            message = "connected successfully"
                            try:
                                self.broker.subscribe(topic)
                            except Exception as e:
                                message = "Error on connect: " + str(e)
                            print(message)
                        else:
                            print("Not connected to MQTT-Broker")
                    else:
                        print("Invalid command format")
            elif input.__len__() > 12:
                if input[:11] == "subscribe":
                    if input[12] == "":
                        topic = input[:13]
                        if self.broker.is_running():
                            message = "connected successfully"
                            try:
                                self.broker.unsubscribe(topic)
                            except Exception as e:
                                message = "Error on connect: " + str(e)
                            print(message)
                        else:
                            print("Not connected to MQTT-Broker")
                    else:
                        print("Invalid command format")

    
    def stop(self):
        self.running = False
        self.broker.stop()
    
    def __init__(self):
        self.broker = mqtt.Broker()
        self.running = False