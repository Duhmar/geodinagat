from django.contrib import admin
from .models import Report, ReportMedia, Profile, Comment

# Only register models that actually live in accounts/models.py
admin.site.register(Report)
admin.site.register(ReportMedia)
admin.site.register(Profile)
admin.site.register(Comment)