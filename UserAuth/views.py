from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import render_to_string
import threading

from .models import User
from Event.models import Event, EventCategory, Team, Member
from api.models import MessageToParticipant
# Create your views here.

def home(request):
	home_page = 'UserAuth/main.html'
	event_cat = EventCategory.objects.all().order_by("web_priority")
	events = Event.objects.all().order_by("web_priority")
	message = MessageToParticipant.objects.all().order_by("-id")
	return render(request, home_page, {"event_category":event_cat, "events":events, "message":message[0] if message else ""})

class UserRegistrationView(View):
	signup_template = 'UserAuth/register.html'
	account_confirmation_page = 'UserAuth/account_confirmation_page.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('Event:events'))
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
			return HttpResponseRedirect(reverse('Event:events'))
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
				return HttpResponseRedirect(reverse('Event:events'))
			return render(request, self.signin_template, {"message":"Wrong email or password."})
		else:
			send_account_activation_url(request, user.username)
			return render(request, self.account_confirmation_page, {"message": "Account is not activated. Please activate your account."})

def send_email(subject, to_email, text_content, html_content):
	from django.core.mail import EmailMultiAlternatives
	# print(subject, to_email, text_content, html_content)
	subject, from_email, to = subject, settings.EMAIL_HOST_USER , to_email
	text_content = text_content
	html_content = html_content
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	print(msg)
	msg.send()
	return

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
	try:
		thread_process = threading.Thread(target=send_email, kwargs={
			"subject":"Abhisarga Account Activation",
			"to_email":user.email,
			"text_content":"",
			"html_content": render_to_string('UserAuth/email_activation_template.html', {"user_fullname":str(user.first_name)+" "+str(user.last_name), "link":activation_url})
			})
		thread_process.start()
	except Exception as e:
		print(e)
	return
	# return render(request, account_confirmation_page)

@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def logout_view(request):
	logout(request)
	return redirect('/')

@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def Profile(request):
	profile_page = 'UserAuth/profile.html'
	if request.method=='GET':
		try:
			participated_events = Team.objects.filter(leader__username=request.user.username)
			part = list()
			for obj in participated_events:
				part.append({"event":obj.event, "team":{"leader": obj,"members": obj.belong_to_team.all()}})

			participated_events = Member.objects.filter(email=request.user.email)
			for obj in participated_events:
				part.append({"event":obj.team.event, "team":{"leader": obj.team,"members": obj.team.belong_to_team.all()}})
		except Exception as e:
			pass
			# print(obj)
		return render(request, profile_page, {"participated_events":part})

def activate_account(request, url):
	try:
		user = User.objects.get(activation_link=url)
		user.activation_link = ""
		user.is_verified = True
		user.save()
		return HttpResponseRedirect(reverse('UserAuth:user_login'))
	except Exception as e:
		return HttpResponseRedirect(reverse('UserAuth:user_login'))


class ForgotPasswordView(View):
	template = "UserAuth/forgot_password.html"

	def get(self, request, *args, **kwargs):
		return render(request, self.template)

	def post(self, request, *args, **kwargs):
		email = request.POST.get('email')
		try:
			user = User.objects.get(email=email)
			url = get_random_string(150)
			absolute_url = request.build_absolute_uri(url)
			activation_url = absolute_url.replace("forgot_password", "reset_password")
			user.activation_link = url
			user.save()
			try:
				thread_process = threading.Thread(target=send_email, kwargs={
					"subject":"Abhisarga Account Password Reset",
					"to_email":user.email,
					"text_content":"",
					"html_content": render_to_string('UserAuth/forgot_password_template.html', {"user_fullname":str(user.first_name)+" "+str(user.last_name), "link":activation_url})
					})
				thread_process.start()
			except Exception as e:
				print(e)
			return render(request, self.template, {"message":"Password reset link is sent to your email. Please check your email."})
		except Exception as e:
			print(e)
			return render(request, self.template, {"message":"Wrong email address."})


def resetPassword(request, url):
	if request.method == 'GET':
		return render(request, "UserAuth/reset_password.html", {"url":url})

	if request.method == 'POST':
		reset_link = url
		password = request.POST.get('password')
		try:
			user = User.objects.get(activation_link=reset_link)
			# print(user)
			if password:
				user.set_password(password)
				user.activation_url=""
				user.save()
			return HttpResponseRedirect(reverse('UserAuth:user_login'))
		except Exception as e:
			print(e)
			return render(request, "UserAuth/forgot_password.html", {"message":"Password reset link expired. Please try again."})