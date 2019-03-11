from django.conf.urls import url
from .views import contactUs, sponsor, team, schedule

app_name = "Other"

urlpatterns = [
	url(r'^contactus/$', contactUs, name='contactus'),
	url(r'^sponsors/$', sponsor, name='sponsors'),
	url(r'^team/$', team, name='team'),
	url(r'^schedule/$', schedule, name='schedule'),
	]