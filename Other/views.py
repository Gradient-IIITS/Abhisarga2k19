from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from .models import TeamCategory, Volunteer
# Create your views here.

def contactUs(request):
	if request.method == 'GET':
		contact_page = 'Other/contact_page.html' 
		return render(request, contact_page)

def sponsor(request):
	if request.method == 'GET':
		return render(request, 'Other/sponsor.html')

def team(request):
	if request.method == 'GET':
		category = TeamCategory.objects.all().order_by("web_priority")
		all_volunteer = list()
		for cat in category:
			volunteers = Volunteer.objects.filter(category__id=cat.id)
			all_volunteer.append({"category":cat, "volunteers":volunteers})
		return render(request, 'Other/team.html', {"objects":all_volunteer})

def schedule(request):
	if request.method == 'GET':
		return render(request, 'Other/schedule.html')
