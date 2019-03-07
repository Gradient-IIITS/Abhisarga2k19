from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def event(request):
	event_template = 'Event/events.html'
	return render(request, event_template)