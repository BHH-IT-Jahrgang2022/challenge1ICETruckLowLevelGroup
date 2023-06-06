import controller as con
import threading
#import api

my_controller = con.Controller()
mqtt_thread = threading.Thread(target=my_controller.start_mqtt)
mqtt_thread.start()

running = True
while running:
    if threading.active_count() <= 2:
        running == False
    else:
        print(threading.active_count())