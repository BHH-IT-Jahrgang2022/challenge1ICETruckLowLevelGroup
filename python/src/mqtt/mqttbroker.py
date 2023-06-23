from paho.mqtt import client as mqtt_client
import logging
import time
import json

# Handles Communication with the MQTT-Broker
class Broker:
    # Connect to MQTT-Broker as Client
    # Return-Code 0 = Successfully connected
    def connect_mqtt(self):
        # nested method of client executed on connection attempt
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Successfully connected to MQTT-Broker")
            else:
                logging.info("Failed to connect to MQTT-Broker with return-code {rc}")
        # Set Connecting Client ID
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        result = 1
        try:
            result = self.client.connect(self.host, self.port)
        except Exception as e:
            logging.error("Failed to connect with: " + str(e))
        if result == 0:
            self.connected = True
        else:
            self.connected = False

    # Disconnection Handling with MQTT-Broker
    # Attempts reconnect according to parameters below
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
                logging.info(f"Send `{message}` to topic `{topic}` on attempt {attempt}")
                break
            else:
                logging.warning(f"Failed to send message to topic {topic}")
                pass
    
    def is_connected(self):
        return self.connected

    # Attempts to connect to MQTT-Broker and starts the Client-Loop if successful
    def connect(self):
        self.connect_mqtt()
        
        if self.connected:
            self.client.loop_start()
    
    # Disconnects from Broker
    def disconnect(self):
        if self.connected:
            self.connected = False
            self.client.loop_stop()
            time.sleep(0.1)
            self.client.disconnect()
            logging.info("Disconnected from MQTT-Broker")

    # Subscribe to a topic on the connected broker
    def subscribe(self, topic:str):
        if self.connected:
            def on_message(client, userdata, msg):
                self.queue.append((msg.topic, msg.payload.decode()))
                logging.info(str(msg.topic) + ": " + str(msg.payload.decode()))
            try:
                self.client.subscribe(topic)
                self.client.on_message = on_message
            except Exception as e:
                logging.info("Could not subscribe to {topic}")
                logging.exception(e)
                return
            logging.info("subscribed to {topic} successfully")
    
    # Attempts to read the config file
    def read_config_file(self):
        configs = {}
        try:
            with open("python/src/mqtt/config.json", "r") as config_file:
                configs = json.loads(config_file.read())
        except Exception as e:
            logging.exception(e)
        return configs
    
    def __init__(self, host=None, client_id=None, port=None, username=None, password=None):
        configs = self.read_config_file()
        # Use input-parameters, if not provided try to read the config-file instead
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
            logging.warning("MQTT-Broker may be improperly configured")

        self.connected = False
        self.queue = []
        self.client = mqtt_client.Client(self.client_id)