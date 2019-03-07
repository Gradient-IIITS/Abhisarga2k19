from django.conf.urls import url
from .views import event

app_name = "Event"

urlpatterns = [
	url(r'^$', event, name='events'),
	]