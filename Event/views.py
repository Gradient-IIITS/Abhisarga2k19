from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout

from .models import EventCategory, Event, Team
# Create your views here.

def event(request):
	event_template = 'Event/events.html'
	event_cat = EventCategory.objects.all()
	all_events = list()
	for _ in event_cat:
		events = Event.objects.filter(event_category__id=_.id)
		all_events.append({"category":_, "events":events})
	participated_events = Team.objects.filter(leader__username=request.user.username)
	part = list()
	for obj in participated_events:
		part.append(obj.event)
	# print(part)
	return render(request, event_template, {"event_category":event_cat, "all_events":all_events, "participated_events":part})


def eventRegistration(request):
	if request.method=='GET':
		event_id = request.GET.get('event_id')
		check = Team.objects.filter(leader__username=request.user.username, event__id=event_id)
		if len(check)==0:
			team = Team()
			team.team_name = request.user.username
			team.event = Event.objects.get(id=event_id)
			team.leader = request.user
			team.save()
		else:
			for _ in check:
				_.delete()

		return HttpResponseRedirect(reverse('Event:events'))


def teamEventRegistration(request):
	pass