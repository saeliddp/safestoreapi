from django.db import models
from jsonfield import JSONField
# Create your models here.
class Store(models.Model):
    zipcode = models.CharField(max_length=20, default="00000")
    physical_address = models.CharField(max_length=100, default="NA")
    name = models.CharField(max_length=100, default="NA")
    latitude = models.CharField(max_length=15, default="0.000000")
    longitude = models.CharField(max_length=15, default="0.000000")
    timetable = JSONField()
    besttime = models.CharField(max_length=10, default="8:00am")
    class Meta:
        ordering = ['id']

    
