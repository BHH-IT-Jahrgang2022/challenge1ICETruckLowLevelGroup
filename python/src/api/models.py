from django.db import models

# toDo: Deprecated, replace with Flask
class Temperature(models.Model):
    timestamp = models.TimeField(auto_now=True)
    temperature = models.FloatField()
    sensor_id = models.CharField()