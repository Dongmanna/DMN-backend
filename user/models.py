# accounts/models.py
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class CustomUser(AbstractUser):
	objects = UserManager()

	nickname = models.CharField(max_length=20)
	address = models.CharField(max_length=50)
	profile_image = ProcessedImageField(
		null = True,
		upload_to = 'static/profile/images',
		processors = [ResizeToFill(300, 300)],
		format = 'JPEG',
		options = {'quality':90},
	)
	
	def __str__(self):
		return self.nickname