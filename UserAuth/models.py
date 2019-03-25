from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

def get_image_upload_path(instance, filename):
	return "Profile/{0}/{1}".format(instance.username, filename)

class User(AbstractUser):
	mobile_no = models.CharField(max_length=15, null=True, blank=True)
	college_name = models.CharField(max_length=100, null=True, blank=True)
	description = models.CharField(max_length=150, null=True, blank=True)
	profile_pic = models.ImageField(upload_to=get_image_upload_path, null=True, blank=True)

	activation_link = models.CharField(max_length=200, null=True, blank=True)
	is_verified = models.BooleanField(default=False)

	device_token = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.username)	