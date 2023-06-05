from django.db import models

# Create your models here.
class Temperature(models.Model):
    timestamp = models.TimeField(auto_now=True)
    temperature = models.FloatField()
    sensor_id = models.CharField()