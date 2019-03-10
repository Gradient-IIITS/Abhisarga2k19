from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.

@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def Accomodation(request):
	accomodation_page = 'Accomodation/accomodation_page.html'
	return render(request, accomodation_page)