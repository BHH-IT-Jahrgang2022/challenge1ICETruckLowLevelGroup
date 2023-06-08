import mqttbroker as mqtt
import threading

class MQTTController:
    def handle_message(self):
        print(self.broker.queue.pop())
    
    def stop_listening(self):
        self.listening = False
    
    def start_listening(self):
        def listen(self):
            while self.listening:
                if self.broker.queue:
                    self.handle_message()
        if not self.listening:
            self.listening = True
            listener_thread = threading.Thread(target=listen)
    
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
                        self.broker.connect()
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
                                target=self.broker.subscribe(topic)
                                self.subscribed_topics.append(topic)
                            except Exception as e:
                                message = "Error on connect: " + str(e)
                            print(message)
                        else:
                            print("Not connected to MQTT-Broker")
                    else:
                        print("Invalid command format")
            elif input.__len__() > 12:
                if input[:11] == "unsubscribe":
                    message = "unsubscribed successfully"
                    if input[12] == "":
                        topic = input[:13]
                        if self.broker.is_running():
                            if topic in self.subscribed_topics:
                                try:
                                    self.broker.unsubscribe(topic)
                                    self.subscribed_topics.remove(topic)
                                except Exception as e:
                                    message = "Error on unsubscribe: " + str(e)
                            else:
                                message = "This topic is not currently subscribed"
                        else:
                            message = "Not connected to MQTT-Broker"
                    else:
                        message = ("Invalid command format")
                    print(message)
            if self.subscribed_topics and not self.listening:
                self.start_listening()
            if self.subscribed_topics.__len__() == 0 and self.listening:
                self.stop_listening()
    
    def stop(self):
        self.running = False
        self.broker.stop()
    
    def __init__(self):
        self.broker = mqtt.Broker()
        self.running = False
        self.listening = False
        self.subscribed_topics = []