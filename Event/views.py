from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import EventCategory, Event, Team, Member
# Create your views here.

def event(request):
	event_template = 'Event/events.html'
	event_cat = EventCategory.objects.all().order_by("web_priority")
	all_events = list()
	for _ in event_cat:
		events = Event.objects.filter(event_category__id=_.id).order_by("web_priority")
		all_events.append({"category":_, "events":events})
	part = list()
	try:
		participated_events = Team.objects.filter(leader__username=request.user.username)
		part = list()
		for obj in participated_events:
			part.append(obj.event)

		participated_events = Member.objects.filter(email=request.user.email)
		for obj in participated_events:
			part.append(obj.team.event)
	except Exception as e:
		pass	
	# print(part)
	return render(request, event_template, {"event_category":event_cat, "all_events":all_events, "participated_events":part})

@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def eventRegistration(request):
	if request.method=='GET':
		event_id = request.GET.get('event_id')
		try:
			event = Event.objects.get(id=event_id)
		except Exception as e:
			print(e)
			return HttpResponseRedirect(reverse('Event:events'))

		if request.user.is_authenticated and not event.registration_closed:
			check = Team.objects.filter(leader__username=request.user.username, event__id=event_id)
			if len(check)==0:
				team = Team()
				team.team_name = request.user.username
				team.event = event
				team.leader = request.user
				team.save()
			else:
				for _ in check:
					_.delete()

			return HttpResponseRedirect(reverse('Event:events'))
		return HttpResponseRedirect(reverse('UserAuth:user_login'))

@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def teamEventRegistration(request):
	if request.method == 'POST':
		team_name = request.POST.get('team_name')
		event_id = request.POST.get('event_id')
		names = request.POST.getlist('name[]')
		emails = request.POST.getlist('email[]')

		try:
			event = Event.objects.get(id=event_id)
		except Exception as e:
			print(e)
			return HttpResponseRedirect(reverse('Event:events'))

		if not event.registration_closed:
			try:
				if request.user.is_authenticated and team_name and event_id:
					team = Team()
					team.team_name = team_name
					team.event = event
					team.leader = request.user
					team.save()

					for name, email in zip(names, emails):
						if name or email:
							member = Member.objects.create(team=team, name=name, email=email)
							member.save()
			except Exception as e:
				print(e)
				return HttpResponseRedirect(reverse('Event:events'))
		return HttpResponseRedirect(reverse('Event:events'))
	pass