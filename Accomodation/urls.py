from django.conf.urls import url
from .views import Accomodation

app_name = "Accomodation"

urlpatterns = [
	url(r'^$', Accomodation, name='accomodation'),
	]