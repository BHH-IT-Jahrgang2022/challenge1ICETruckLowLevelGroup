

class MQTTController:
    def start(self):
        self.running = True
        self.loop()
    
    def loop(self):
        while self.running:
            pass
    
    def stop(self):
        self.running = False
    
    def __init__(self):
        self.running = False