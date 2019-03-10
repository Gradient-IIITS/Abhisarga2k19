from django.db import models

# Create your models here.

def get_avatar_path(instance, filename):
	return "Volunteer/{0}/{1}".format(instance.name, filename)

class TeamCategory(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.name


class Volunteer(models.Model):
	category = models.ForeignKey(TeamCategory, on_delete=models.CASCADE, related_name="team")
	name = models.CharField(max_length=200, null=True, blank=True)
	avatar = models.ImageField(upload_to=get_avatar_path, null=True, blank=True)
	description = models.TextField()
	designation = models.CharField(max_length=200, null=True, blank=True)
	mobile_no = models.CharField(max_length=100, null=True, blank=True)
	email = models.CharField(max_length=100, null=True, blank=True)
	facebook_link = models.CharField(max_length=200, null=True, blank=True)
	instagram_link = models.CharField(max_length=200, null=True, blank=True)
	linkedin_link = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.name