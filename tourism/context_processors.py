# tourism/context_processors.py
from .models import TouristSpot, TransportationTerminal

def global_map_locations(request):
    try:
        # Fetch all locations from your database
        tourist_spots = TouristSpot.objects.exclude(latitude__isnull=True, longitude__isnull=True)
        terminals = TransportationTerminal.objects.exclude(latitude__isnull=True, longitude__isnull=True)
    except Exception:
        tourist_spots = []
        terminals = []
        
    return {
        'db_tourist_spots': tourist_spots,
        'db_terminals': terminals
    }