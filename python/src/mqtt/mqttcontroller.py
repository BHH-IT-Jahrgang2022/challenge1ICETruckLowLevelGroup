import mqttbroker as mqtt
import threading

class MQTTController:
    def stop_mqtt():
        self.mqtt_running = False

    def start_mqtt(self):    
        connected = False
        try:
            client = self.broker.connect_mqtt()
            self.broker.subscribe("sensors/ESP32Sense1/data/", client)
            connected = True
        except Exception as e:
            connected = False
            print(e)

        if connected:
            broker_thread = threading.Thread(target=client.loop_forever)

            broker_thread.start()

            self.mqtt_running = True
            print("I work")
            while self.mqtt_running:
                if self.broker.queue:
                    payload = self.broker.queue.pop(0)
                    print(payload)
            broker_thread._stop()
            broker_thread._delete()

    def start(self):
        self.running = True
        self.start_mqtt()
        self.loop()
    
    def loop(self):
        while self.running:
            pass
    
    def stop(self):
        self.running = False
        self.mqtt_running = False
    
    def __init__(self):
        self.broker = mqtt.Broker()
        self.running = False
        self.mqtt_running = False