# main/models.py
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import Profile
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class Post(models.Model):
    objects = models.Manager()
    author = models.ForeignKey(Profile, blank=True, null=True,
                               on_delete=models.CASCADE, related_name='author_post')
    category = models.CharField(max_length=20,
                                choices=(
                                    ('Offline', '오프라인'),
                                    ('Online', '온라인'),
                                    ('Delivery', '배달음식'),
                                ))
    title = models.CharField(max_length=150)
    pub_date = models.DateTimeField(default=timezone.now)
    body = models.TextField(default='')
    region = models.CharField(max_length=50, blank=True, null=True)
    item = models.CharField(max_length=50)
    limit = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    link = models.URLField(max_length=300, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    members = models.ManyToManyField(
        Profile, blank=True, related_name='members_post')
    # 사진 1개 받기
    image = ProcessedImageField(
    		blank = True,
        	upload_to = 'post/images',
        	processors = [ResizeToFit(300, 300)],
        	format = 'JPEG',
        	options = {'quality':90},
    		)

    def __str__(self):
        return self.title