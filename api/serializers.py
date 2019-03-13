from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from UserAuth.models import *
from Event.models import *

class UserSerializer(ModelSerializer):

	profile_pic = serializers.SerializerMethodField('get_thumbnail_url')
	def get_thumbnail_url(self, obj):
		try:
			return self.context['request'].build_absolute_uri(obj.profile_pic.url)
		except:
			return None

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
	brochure = serializers.SerializerMethodField('get_thumbnail_url')

	def get_thumbnail_url(self, obj):
		try:
			return self.context['request'].build_absolute_uri(obj.brochure.url)
		except:
			return None
	
	class Meta:
		model = Event
		fields = '__all__'