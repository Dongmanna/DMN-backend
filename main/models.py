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
    # 자동입력 필드: 작성자, 작성일시, 지역
    author = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='post_author')
    pub_date = models.DateTimeField(default=timezone.now)
    region = models.CharField(max_length=50, blank=True, null=True)
    
    # 필수 필드: 카테고리, 제목, 글내용, 품목, 정원(1-10명)
    category = models.CharField(max_length=20,
                                choices=(
                                    ('Offline', '오프라인'),
                                    ('Online', '온라인'),
                                    ('Delivery', '배달음식'),
                                ))
    title = models.CharField(max_length=150)
    body = models.TextField(default='')
    item = models.CharField(max_length=50)
    limit = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    # 비필수 필드: 링크, 가격, 마감기한, 사진
    link = models.URLField(max_length=300, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    image = ProcessedImageField(
    		null = True,
        	upload_to = 'post/images',
        	processors = [ResizeToFit(300, 300)],
        	format = 'JPEG',
        	options = {'quality':90},
    		)
    
    # 공동구매 참여자
    members = models.ManyToManyField(
        CustomUser, blank=True, related_name='members')
    # 공동구매 완료 여부
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