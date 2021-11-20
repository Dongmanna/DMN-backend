# main/serializers.py
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from rest_framework import serializers
from main.models import Post, DoneRegister, Comment
from user.serializers import UserSerializer


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    title = serializers.CharField(
        validators=[MaxLengthValidator(150)]
    )
    region = serializers.CharField(read_only=True, source='author.address')
    item = serializers.CharField(
        validators=[MaxLengthValidator(50)]
    )
    limit = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['url', 'id', 'author', 'category', 'title', 'pub_date', 
        'body', 'region', 'item', 'limit', 'link', 'deadline', 'members', 'image', 'done']
        read_only_fields = ['author', 'pub_date', 'done', 'members']


class DoneRegisterSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = DoneRegister
        fields = ['post', 'users']
        read_only_fields = ['post', 'users']



class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['url', 'id', 'post', 'author', 'pub_date', 'content']
        read_only_fields = ['author', 'pub_date',]