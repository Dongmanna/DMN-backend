from rest_framework import serializers
from main.models import Post
from user.serializers import UserSerializer


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.DateTimeField(read_only=True)
    region = serializers.CharField(source='author.address')
    members = UserSerializer(read_only=True, many=True)
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Post
        fields = ['url', 'id', 'author', 'category', 'title', 'pub_date', 
        'body', 'region', 'item', 'limit', 'link', 'deadline', 'members', 'image']