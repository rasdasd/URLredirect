from django.db import models
from django.utils import timezone

# Create your models here.

class HashedURL(models.Model):
	hash = models.CharField(max_length=7)
	url = models.CharField(max_length=1000)
	timestamp = models.DateTimeField(default=timezone.now)
	ip = models.GenericIPAddressField()

	def __str__(self):
		return  self.hash + ' ' + self.url

class Redirect(models.Model):
	hashedUrl = models.ForeignKey(HashedURL)
	referer = models.CharField(max_length=1000)
	user_agent = models.CharField(max_length=200)
	timestamp = models.DateTimeField(default=timezone.now)
	ip = models.GenericIPAddressField()

	def __str__(self):
		return str(self.hashedUrl)[:30] + ' ' + self.referer[:30]