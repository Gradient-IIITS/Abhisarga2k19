from django.conf.urls import url
from .views import contactUs, sponsor, team, schedule, proshow
from .utils import some_streaming_csv_view

app_name = "Other"

urlpatterns = [
	url(r'^contactus/$', contactUs, name='contactus'),
	url(r'^sponsors/$', sponsor, name='sponsors'),
	url(r'^proshows/$', proshow, name='proshows'),
	url(r'^team/$', team, name='team'),
	url(r'^schedule/$', schedule, name='schedule'),
	url(r'^csv_download/$', some_streaming_csv_view, name='csv_download'),
	]