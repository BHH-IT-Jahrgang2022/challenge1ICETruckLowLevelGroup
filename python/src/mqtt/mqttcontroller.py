import mqttbroker as mqtt
import threading
import time
import json

class MQTTController:
    def save_temp(self, temp):
        try:
            print(temp)
            # integer conversion converts Python Unix with Mili to standard Unix-Second-Timestamp
            data_to_save = {'timestamp': int(time.time()), 'sensor_id': "sens_01", 'temperature': float(temp)}
            print(data_to_save)
            json_data = json.dumps(data_to_save)
        except Exception as e:
            print(e)

    def stop_listening(self):
        self.listening = False
    
    def start_listening(self):
        def listen():
            while self.listening:
                time.sleep(0.01)
                if self.broker.queue:
                    topic, temp = self.broker.queue.pop()
                    print(topic)
                    print(temp)
                    # integer conversion converts Python Unix with Mili to standard Unix-Second-Timestamp
                    data_to_save = {'timestamp': int(time.time()), 'sensor_id': "sens_01", 'temperature': float(temp)}
                    print(data_to_save)
                    json_data = json.dumps(data_to_save)
                    #self.save_temp(self.broker.queue.pop())
        if not self.listening:
            self.listening = True
            listener_thread = threading.Thread(target=listen)
            listener_thread.start()
    
    def start(self):
        self.running = True
        self.start_listening()
        self.loop()
    
    def loop(self):
        while self.running:
            input1 = ""
            input1 = input("Commands: stop, connect, subscribe [topic], unsubscribe [topic], publish [topic] [value] \n")
            print(input1)
            if (input1.__len__() > 8):
                print(input1[:7])
                print(input1[8:])
            if input1 == "stop":
                if self.broker.is_connected():
                    message = "disconnected successfully"
                    try:
                        self.stop()
                    except Exception as e:
                        message = "Error on disconnect: " + str(e)
                    print(message)
            elif input1 == "connect":
                if self.broker.is_connected():
                    print("MQTT-Broker is already running!")
                else:
                    message = self.broker.connect()
                    time.sleep(1)
                    if self.broker.is_connected():
                        message += "connected successfully"
                    print(message)
            elif input1.__len__() > 9:
                if input1[:9] == "subscribe":
                    if input1[9] == " ":
                        topic = input1[10:]
                        if self.broker.is_connected():
                            message = "subscribed successfully"
                            try:
                                self.broker.subscribe(topic)
                                self.subscribed_topics.append(topic)
                            except Exception as e:
                                message = "Error on connect: " + str(e)
                            print(message)
                        else:
                            print("Not connected to MQTT-Broker")
                    else:
                        print("Invalid command format")
            elif input1.__len__() > 11:
                if input1[:11] == "unsubscribe":
                    message = "unsubscribed successfully"
                    if input1[11] == " ":
                        topic = input1[12:]
                        if self.broker.is_connected():
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
            elif input1.__len__() > 8:
                if input1[:7] == "publish":
                    if input1[7] == " ":
                        topic, value = input1[8:].split(" ")
                        if self.broker.is_connected():
                            message = "subscribed successfully"
                            try:
                                self.broker.publish(topic, value)
                                self.subscribed_topics.append(topic)
                            except Exception as e:
                                message = "Error on connect: " + str(e)
                            print(message)
                        else:
                            print("Not connected to MQTT-Broker")
                    else:
                        print("Invalid command format")
            else:
                print("No valid command entered")
            if self.subscribed_topics and not self.listening:
                #self.start_listening()
                pass
            if self.subscribed_topics.__len__() == 0 and self.listening:
                #self.stop_listening()
                pass
    
    def stop(self):
        self.running = False
        self.stop_listening()
        time.sleep(1)
        self.broker.disconnect()
    
    def __init__(self):
        self.broker = mqtt.Broker("pi-johanna.local",f"pi0")
        self.running = False
        self.listening = False
        self.subscribed_topics = []