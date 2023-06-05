import time
import mqttbroker as mqtt
import databasemanager as dbm
import threading
          
class Controller:
    def save(data):
        if data == None:
            return False
        
        #Todo: deserialization of sensor data
        
        self.db_manager.persist(Temperature(temperature=data, sensor_id=data))
    
    def load(queryset=dict):
        if not queryset:
            return False
        self.db_manager.load(Temperature, queryset)
        return True
    
    def update(primary_key, change_key, change_value):
        temperature_object = self.load({"timestamp": primary_key})
        self.db_manager.update(temperature_object, change_key, change_value)
    
    def stop_mqtt():
        self.mqtt_running = False
        
    
    def start_mqtt(self):    
        connected = False
        try:
            client = self.mqtt_broker.connect_mqtt()
            self.broker.subscribe(client)
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
                if broker.queue:
                    payload = broker.queue.pop(0)
                    print(payload)
            else:
                broker_thread._stop()
    
    def __init__(self):
        print("I've been initialized")
        self.db_manager = dbm.DatabaseManager()
        self.mqtt_broker = mqtt.Broker()
        self.mqtt_running = False