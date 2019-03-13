from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from UserAuth.models import User
from Event.models import Event, Team, Member
from .models import MessageToParticipant
from .serializers import UserSerializer, EventSerializer, MessageSerializer

import json

class UserView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		try:
			serialized_user = UserSerializer(request.user, many=False, context={"request":request})
			return Response(serialized_user.data)
		except Exception as e:
			return Response("User does not exists.")


class EventView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		try:
			events = Event.objects.all()
			serialized_events = EventSerializer(events, many=True, context={"request":request})
			return Response(serialized_events.data)
		except Exception as e:
			print(e)
			return Response("Something went wrong.")

class CheckRegistrationView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		try:
			event_id = request.GET.get('event_id')
			username = request.GET.get('username')
			participated_event = True if Team.objects.filter(leader__username=username, event__id=event_id).count() else False
			print ("participated_event", participated_event)
			return Response(participated_event)
		except Exception as e:
			print(e)
			return Response("Something went wrong.")


		# print ("request is", request.GET.get('event_id'))
	
class RegisterForTeamEventView(APIView):
	permission_classes = (AllowAny,)

	def post(self, request, format=None):
		try:
			body = json.loads(request.body.decode('utf-8'))
			event_id = body['event_id']
			form = body['form']
			print('form, event_id', form, event_id)

			team = Team()
			team.team_name = form['team_name']
			team.event = Event.objects.get(id=event_id)
			team.leader = request.user
			team.save()

			for key in form.keys():
				if key != "team_name" and key != "leader":
					print ("key, form[key]", key, form[key])
					member = Member.objects.create(team=team, name=form[key], email=form[key])
			return Response(True)
		except Exception as e:
			print (e)
			return Response(False)

class RegisterForSingleEventView(APIView):
	permission_classes = (AllowAny,)

	def post(self, request, format=None):
		try:
			body = json.loads(request.body.decode('utf-8'))
			event_id = body['event_id']
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
			return Response(True)
		except Exception as e:
			print (e)
			return Response(False)


class MessageFromTeamView(APIView):
	permission_classes = (AllowAny,)
	def get(self, request, format=None):
		try:
			message = MessageToParticipant.objects.all()
			serialized_message = MessageSerializer(message, many=True)
			return Response(serialized_message.data)
		except Exception as e:
			print(e)
			return Response("Something went wrong.")

			# return Response({'bold_heading': "Abhisarga starts in 29th March",
			# 				'content': "Welcome to Abhisarga, 2k19. The annual cultural fest of IIIT Sri City. This years its bigger than ever.",
			# 				"issued_by": "Bhavi Chawla",
			# 				"sub_heading": "Message from the abhisarga team"})