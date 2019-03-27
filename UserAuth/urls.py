from django.conf.urls import url
from .views import UserRegistrationView, UserLoginView, activate_account, logout_view, home, Profile, ForgotPasswordView, resetPassword

app_name = "UserAuth"

urlpatterns = [
	url(r'^$', home, name='home'),
	url(r'^signup/$', UserRegistrationView.as_view(), name='user_registration'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^signin/$', UserLoginView.as_view(), name='user_login'),
	url(r'^profile/$', Profile, name='profile'),
	url(r'^forgot_password/$', ForgotPasswordView.as_view(), name='forgot_password'),
	url(r'^reset_password/(?P<url>[0-9a-zA-z]+)/$', resetPassword, name='reset_password'),
	url(r'^activate_account/(?P<url>[0-9a-zA-z]+)/$', activate_account, name='activate_account'),
	]