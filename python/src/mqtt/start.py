import threading
import mqttcontroller as con
import time

mqqt_controller = con.MQTTController()
mqqt_thread = threading.Thread(target=mqqt_controller.start)
mqqt_thread.start()

time.sleep(10)

mqqt_controller.stop()
