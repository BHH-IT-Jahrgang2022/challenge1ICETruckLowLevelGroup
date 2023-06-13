from paho.mqtt import client as mqtt_client
import logging
import time
import json

class Broker:
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Error on connect?")
        # Set Connecting Client ID
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        result = self.client.connect(self.host, self.port)
        #print(result)

    def on_disconnect(self, client, userdata, rc):
        FIRST_RECONNECT_DELAY = 1
        RECONNECT_RATE = 2
        MAX_RECONNECT_COUNT = 12
        MAX_RECONNECT_DELAY = 60
        self.connected = False
        
        logging.info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            logging.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                self.client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

    def publish(self, topic, message):
        for attempt in range(0, 5):
            time.sleep(1)
            result = self.client.publish(topic, message)
            status = result[0]
            if status == 0:
                #print(f"Send `{message}` to topic `{topic}` on attempt {attempt}")
                break
            else:
                #print(f"Failed to send message to topic {topic}")
                pass
        
    def is_connected(self):
        return self.connected

    def connect(self):
        message = ""
        try:
            self.connect_mqtt()
            self.connected = True
        except Exception as e:
            self.connected = False
            message = str(e)
        
        self.client.loop_start()

        return message
        
        #if self.connected:
            #broker_thread = threading.Thread(target=self.client.loop_start())
            #broker_thread.start()
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            self.client.loop_stop()
            self.client.disconnect()
            time.sleep(1)

    def subscribe(self, topic):
        if self.connected:
            def on_message(client, userdata, msg):
                self.queue.append((msg.topic, msg.payload.decode()))
                #print(msg.payload.decode())
            try:
                #self.client.loop_stop()
                self.client.subscribe(topic)
                self.client.on_message = on_message
                #self.client.loop_start()
                #print(topic)
                #print(self.client.is_connected())
            except Exception as e:
                #print("Subscribe failed with: " + str(e))
                return
            #print("subscribed successfully")
    
    def __init__(self, host=None, client_id=None, port=None, username=None, password=None):
        configs = {}
        try:
            with open("python/src/mqtt/config.json", "r") as config_file:
                configs = json.loads(config_file.read())
        except Exception as e:
            #print("Couldn't open config.json, implement it or pass the values through the constructor.")
            print(e)
        
        #print(configs)
        
        if host == None: self.host = configs['host']
        else: self.host = host
        if client_id == None: self.client_id = configs['client_id']
        else: self.client_id = client_id
        if port == None: self.port = configs['port']
        else: self.port = port
        if username == None: self.username = configs['username']
        else: self.username = username
        if password == None: self.password = configs['password']
        else: self.password = password
        
        if self.host == None or self.client_id == None or self.port == None:
            print("mqtt_broker may be improperly configured")

        self.connected = False
        self.queue = []
        self.client = mqtt_client.Client(self.client_id)