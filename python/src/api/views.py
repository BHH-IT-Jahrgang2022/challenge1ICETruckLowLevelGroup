from django.http import HttpResponse
from django.views.generic import ListView
import django.views.generic as dv

def test(request):
    return HttpResponse("I live")

#ToDo: Abfrage aller Daten
#ToDo: Abfrage in einem Zeitintervall
#ToDo: Abfrage zu einem Sensor
#ToDo: Kombinationen
class ThermalData(ListView):
    def get_all_data(self, *args, **kwargs):
        self.get_queryset()
        return HttpResponse("all Data")
    
    def get_temp_in_time_interval(self, *args, **kwargs):
        return HttpResponse("all Data")
    
    def get_temp_for_timestamp(self, *args, **kwargs):
        return HttpResponse("all Data")
    
    def get_temp_for_sensor_id(self, *args, **kwargs):
        return HttpResponse("all Data")