from django.conf.urls import url
from .views import event, eventRegistration

app_name = "Event"

urlpatterns = [
	url(r'^$', event, name='events'),
	url(r'^eventRegistration/$', eventRegistration, name='eventRegistration'),
	]