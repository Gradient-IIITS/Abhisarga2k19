from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout

from .models import User
from Event.models import Event, EventCategory
# Create your views here.

def home(request):
	home_page = 'UserAuth/main.html'
	event_cat = EventCategory.objects.all()
	events = Event.objects.all()
	return render(request, home_page, {"event_category":event_cat, "events":events})

class UserRegistrationView(View):
	signup_template = 'UserAuth/register.html'
	account_confirmation_page = 'UserAuth/account_confirmation_page.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.signup_template)
		
	def post(self, request, *args, **kwargs):
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		mobile_no = request.POST.get('mobile_no')
		college_name = request.POST.get('college_name')
		description = request.POST.get('description')
		password = request.POST.get('password')

		if password:
			try:
				user = User()
				user.username = email.split('@')[0]
				user.first_name = first_name
				user.last_name = last_name
				user.email = email
				user.mobile_no = mobile_no
				user.college_name = college_name
				user.description = description
				user.set_password(password)
				user.save()

				send_account_activation_url(request, user.username)
				return render(request, self.account_confirmation_page)
			except Exception as e:
				print(e)
				return render(request, self.signup_template, {"message":"User is already registered."})
		return render(request, self.signup_template, {"message":"Something went wrong."})


class UserLoginView(View):
	signin_template = 'UserAuth/login.html'
	account_confirmation_page = 'UserAuth/account_confirmation_page.html'
	homepage = 'Event/events.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return render(request, self.homepage)
		return render(request, self.signin_template)

	def post(self, request, *args, **kwargs):
		email = request.POST.get('email')
		password = request.POST.get('password')
		try:
			user = User.objects.get(username=email.split('@')[0])
		except:
			return render(request, self.signin_template, {"message":"Wrong email or password."})
		if user.is_verified:
			user = authenticate(username=user.username, password=password)
			if user is not None:
				login(request, user)
				if request.GET.get('next'):
					return redirect(request.GET.get('next'))
				return render(request, self.homepage)
			return render(request, self.signin_template, {"message":"Wrong email or password."})
		else:
			return render(request, self.account_confirmation_page, {"message": "Account is not activated. Please activate your account."})

def send_account_activation_url(request, username):
	account_confirmation_page = 'UserAuth/account_confirmation_page.html'
	user = get_object_or_404(User, username=username)
	url = get_random_string(150)
	absolute_url = request.build_absolute_uri(url)
	activation_url = absolute_url.replace("signin", "activate_account")
	activation_url = activation_url.replace("signup", "activate_account")
	print(activation_url)
	user.activation_link = url
	user.save()
	# send_email()
	return render(request, account_confirmation_page)


def logout_view(request):
	logout(request)
	return redirect('/')

def activate_account(request, url):
	try:
		user = User.objects.get(activation_link=url)
		user.activation_link = ""
		user.is_verified = True
		user.save()
		return render(request, 'UserAuth/signin.html', {"message": "Account activated."})
	except:
		return HttpResponse("Activation link has expired.")