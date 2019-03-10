from django.conf.urls import url
from .views import contactUs

app_name = "Other"

urlpatterns = [
	url(r'^contactus/$', contactUs, name='contactus'),
	]