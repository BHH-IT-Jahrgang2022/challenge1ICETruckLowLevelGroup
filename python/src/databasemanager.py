
class DatabaseManager:
    def persist(self, model_object):
        model_object.save()
    
    def load(self, model_type, queryset=dict):
        return model_type.objects.get(**queryset)
    
    def update(self, model_object, change_key, change_value):
        model_object.change_key = change_value
        self.persist(model_object)
    
    def __init__(self, database):
        self.database = database