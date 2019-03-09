from django.conf.urls import url
from .views import UserView, EventView

app_name = 'api'

urlpatterns = [
	url(r'^user/$', UserView.as_view(), name='user'),
	url(r'^events/$', EventView.as_view(), name='events'),
	]