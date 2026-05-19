from django.db import models
from django.contrib.auth.models import User

class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    name = models.CharField(max_length=200)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='accommodations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_fully_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.municipality.name})"

class TouristSpot(models.Model):
    CATEGORY_CHOICES = [
        ('BEACH', 'Beach/Resort'),
        ('LAGOON', 'Lagoon/Pool'),
        ('ISLET', 'Islet/Island'),
        ('NATURE', 'Forest/Cave/Rock Formation'),
        ('HISTORICAL', 'Historical/Shrine'),
    ]
    name = models.CharField(max_length=200)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='tourist_spots', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='BEACH')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class TransportationTerminal(models.Model):
    TERMINAL_TYPES = [
        ('PORT', 'Seaport'),
        ('HABAL_HABAL', 'Habal-Habal Terminal'),
    ]
    name = models.CharField(max_length=200)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='transport_terminals', null=True, blank=True)
    terminal_type = models.CharField(max_length=20, choices=TERMINAL_TYPES, default='PORT')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_terminal_type_display()})"