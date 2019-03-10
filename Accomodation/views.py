from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.

def Accomodation(request):
	accomodation_page = 'Accomodation/accomodation_page.html'
	return render(request, accomodation_page)