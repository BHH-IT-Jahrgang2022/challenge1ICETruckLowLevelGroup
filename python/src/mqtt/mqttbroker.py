from paho.mqtt import client as mqtt_client
import threading

class Broker:
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        self.client = mqtt_client.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(broker, port)

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
                print(f"Send `{message}` to topic `{topic}` on attempt {attempt}")
                break
            else:
                print(f"Failed to send message to topic {topic}")
        
    def is_connected(self):
        return self.connected

    def connect(self):    
        try:
            self.client = self.broker.connect_mqtt()
            self.connected = True
        except Exception as e:
            self.connected = False
            print(e)

        if self.connected:
            broker_thread = threading.Thread(target=self.client.loop_forever)
            broker_thread.start()
    
    def disconnect(self):
        if self.connected:
            try:
                self.client.disconnect()
                self.connected = False
            except Exception as e:
                print("fatal error on disconnect: {e}")

    def subscribe(self, topic):
        if self.connected:
            def on_message(client, userdata, msg):
                self.queue.append(msg.payload.decode())
            self.client.subscribe(topic)
            self.client.on_message = on_message
    
    def __init__(self, broker, client_id, port=1883, username="", password=""):
        self.broker = 'pi-johanna.local'
        self.client_id = f'pi0'
        self.port = 1883
        self.username = 'low_level'
        self.password = 'mqttguys'
        
        self.connected = False
        self.queue = []
        self.client = None