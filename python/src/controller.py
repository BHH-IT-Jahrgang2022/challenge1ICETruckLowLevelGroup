
class Controller:
    def save(data):
        if data == None:
            return False
        self.db_manager.persist(data)
                
    
    def __init__(self, database_manager):
        self.db_manager = database_manager
        pass