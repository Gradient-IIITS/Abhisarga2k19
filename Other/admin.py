from django.contrib import admin

from .models import TeamCategory, Volunteer, Sponsor
# Register your models here.

admin.site.register(TeamCategory)
admin.site.register(Volunteer)
admin.site.register(Sponsor)