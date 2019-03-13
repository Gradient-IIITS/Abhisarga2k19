from django.conf.urls import url
from .views import UserView, EventView, CheckRegistrationView, RegisterForTeamEventView

app_name = 'api'

urlpatterns = [
	url(r'^user/$', UserView.as_view(), name='user'),
	url(r'^events/$', EventView.as_view(), name='events'),
	url(r'^check-registration/$', CheckRegistrationView.as_view(), name='CheckRegistration'),
	url(r'^register-for-team-event/$', RegisterForTeamEventView.as_view(), name='RegisterForTeamEventView'),


	


	
	]