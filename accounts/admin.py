from django.contrib import admin
from .models import Report, ReportMedia, Profile, Comment, Hotel, RoomBooking

# Registering your existing models
admin.site.register(Report)
admin.site.register(ReportMedia)
admin.site.register(Profile)
admin.site.register(Comment)

# Registering the new Hotel and Booking models
admin.site.register(Hotel)
admin.site.register(RoomBooking)