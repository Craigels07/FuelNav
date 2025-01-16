from django.db import models

class Truckstop(models.Model):
    opis_id = models.IntegerField()
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    rack_id = models.IntegerField()
    retail_price = models.FloatField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state})"
