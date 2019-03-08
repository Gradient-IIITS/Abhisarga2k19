from django.contrib import admin
from .models import Event, Team, Member, EventCatalogue, EventCategory

# Register your models here.
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(Member)
admin.site.register(EventCatalogue)
admin.site.register(EventCategory)