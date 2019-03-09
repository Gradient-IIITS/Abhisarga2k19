from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from UserAuth.models import *
from Event.models import *

class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'mobile_no',
			'college_name',
			'description',
			'profile_pic',
			'is_verified'
			]
		extra_kwargs = {
			'password': {'write_only':True}
		}


class EventCategorySerializer(ModelSerializer):
	class Meta:
		model = EventCategory
		fields = '__all__'


class EventSerializer(ModelSerializer):
	event_category = EventCategorySerializer(many=False, required=False)
	organisers = UserSerializer(many=True, required=False)
	
	class Meta:
		model = Event
		fields = '__all__'