# users/models.py
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class CustomUser(AbstractUser):
	objects = UserManager()

	# 상속받은 AbstractUser에서 사용하지 않는 필드는 None으로 변경
	first_name = None
	last_name = None
	username = None
	# username을 대신해서 email이 그 역할을 할 것이므로 unique = True
	email = models.EmailField(unique=True)

	# username을 email이 대체 
	USERNAME_FIELD = 'email'
	# nickname과 address는 필수 입력
	REQUIRED_FIELDS = ['nickname', 'address']

	# 추가한 필드
	nickname = models.CharField(max_length=20, unique=True)
	address = models.CharField(max_length=50)
	profile_image = ProcessedImageField(
		null = True,
		blank = True,
		upload_to = 'static/profile/images',
		processors = [ResizeToFill(300, 300)],
		format = 'JPEG',
		options = {'quality':90},
	)
	
	def __str__(self):
		return self.nickname