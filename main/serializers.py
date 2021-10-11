from rest_framework import serializers
from main.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['url', 'id', 'category', 'title', 'pub_date', 'body', 'region', 'item', 'limit', 'link', 'deadline']