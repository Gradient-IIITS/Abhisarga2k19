from django.conf.urls import url
from .views import event, eventRegistration, teamEventRegistration, eventTeamEdit

app_name = "Event"

urlpatterns = [
	url(r'^$', event, name='events'),
	url(r'^eventRegistration/$', eventRegistration, name='eventRegistration'),
	url(r'^teamEventRegistration/$', teamEventRegistration, name='teamEventRegistration'),
	url(r'^eventTeamEdit/$', eventTeamEdit, name='eventTeamEdit'),
	]