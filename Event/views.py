from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout

from .models import EventCategory, Event
# Create your views here.

def event(request):
	event_template = 'Event/events.html'
	event_cat = EventCategory.objects.all()
	all_events = list()
	for _ in event_cat:
		events = Event.objects.filter(event_category__id=_.id)
		all_events.append({"category":_, "events":events})
	return render(request, event_template, {"event_category":event_cat, "all_events":all_events})