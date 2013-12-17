from django.contrib import admin
from PointsOfInterest.models import PointOfInterest, Friend
from django.contrib.auth.models import User

admin.site.register(PointOfInterest)
admin.site.register(Friend)
# Register your models here.
