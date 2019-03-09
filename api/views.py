from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from UserAuth.models import User
from Event.models import Event
from .serializers import UserSerializer, EventSerializer


class UserView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		try:
			serialized_user = UserSerializer(request.user, many=False)
			return Response(serialized_user.data)
		except Exception as e:
			return Response("User does not exists.")


class EventView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		try:
			events = Event.objects.all()
			serialized_events = EventSerializer(events, many=True)
			return Response(serialized_events.data)
		except Exception as e:
			print(e)
			return Response("Something went wrong.")