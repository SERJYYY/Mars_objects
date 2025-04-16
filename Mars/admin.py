from django.contrib import admin
from .models import MarsObject, MarsRequest, RequestItem, Rover

admin.site.register(MarsObject)
admin.site.register(MarsRequest)
admin.site.register(RequestItem)
admin.site.register(Rover)
