from django.conf.urls import url
from .views import UserRegistrationView, UserLoginView, activate_account, logout_view, home

app_name = "UserAuth"

urlpatterns = [
	url(r'^$', home, name='home'),
	url(r'^signup/$', UserRegistrationView.as_view(), name='user_registration'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^signin/$', UserLoginView.as_view(), name='user_login'),
	url(r'^activate_account/(?P<url>[0-9a-zA-z]+)/$', activate_account, name='activate_account'),
	]