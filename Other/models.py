from django.db import models

# Create your models here.

def get_avatar_path(instance, filename):
	return "Volunteer/{0}/{1}".format(instance.name, filename)

def get_sponsor_path(instance, filename):
	return "Sponsor/{0}/{1}".format(instance.name, filename)

class TeamCategory(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	web_priority = models.IntegerField(default=0)
	app_priority = models.IntegerField(default=0)

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
	web_priority = models.IntegerField(default=0)
	app_priority = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class SponsorCategory(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	web_priority = models.IntegerField(default=0)
	app_priority = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class Sponsor(models.Model):
	category = models.ForeignKey(SponsorCategory, on_delete=models.CASCADE, related_name="sponsor_names")
	name = models.CharField(max_length=100, null=True, blank=True)
	website = models.CharField(max_length=100, null=True, blank=True)
	logo = models.ImageField(upload_to=get_sponsor_path, null=True, blank=True)
	web_priority = models.IntegerField(default=0)
	app_priority = models.IntegerField(default=0)

	def __str__(self):
		return self.name