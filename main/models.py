# main/models.py
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import CustomUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class Post(models.Model):
    objects = models.Manager()
    # on_delete=models.CASCADE -> 유저가 삭제될 때 글도 같이 삭제될 것인지 논의 필요
    author = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='post_author')
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
    # 공동구매 모집 인원수 (1~10명)
    limit = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    link = models.URLField(max_length=300, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    # 공동구매 참여자
    members = models.ManyToManyField(
        CustomUser, blank=True, related_name='members')
    # 사진 1개 받기
    image = ProcessedImageField(
    		null = True,
        	upload_to = 'static/post/images',
        	processors = [ResizeToFit(300, 300)],
        	format = 'JPEG',
        	options = {'quality':90},
    		)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class DoneRegister(models.Model):
    objects = models.Manager()
    post = models.OneToOneField('Post', on_delete=models.CASCADE, related_name='done_post')
    users = models.ManyToManyField(
        CustomUser, blank=True, related_name='done_users')


class Comment(models.Model):
    objects = models.Manager()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comment_post')
    # on_delete=models.CASCADE -> 유저가 삭제될 때 댓글도 같이 삭제될 것인지 논의 필요
    author = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='comment_author')
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.TextField(default='')