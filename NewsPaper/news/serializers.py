from rest_framework import serializers

from .models import Post


class PostsSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category']