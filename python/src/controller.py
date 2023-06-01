import time
from model import *
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
    
    def __init__(self, database_manager):
        self.db_manager = database_manager