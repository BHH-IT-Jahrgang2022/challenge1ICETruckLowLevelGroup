import threading
import mqttcontroller as con
import time

mqtt_controller = con.MQTTController()
mqtt_controller.start()