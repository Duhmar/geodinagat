from django.contrib import admin
from .models import Municipality, Accommodation, TouristSpot, TransportationTerminal

admin.site.register(Municipality)
admin.site.register(Accommodation)
admin.site.register(TouristSpot)
admin.site.register(TransportationTerminal)