from django.contrib import admin
from .models import StudentProfile, Preferences, RoomListing

admin.site.register(StudentProfile)
admin.site.register(Preferences)
admin.site.register(RoomListing)
