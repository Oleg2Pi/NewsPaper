from django_filters import FilterSet
from .models import Post


class PostsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'name': ['icontains',],
            'author': ['icontains',],
            'time_created': ['gt',],
        }