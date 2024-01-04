from django_filters import FilterSet, CharFilter, DateFilter
from django.forms import DateInput
from .models import Post


class PostsFilter(FilterSet):
    date = DateFilter(
        field_name= 'time_create',
        label='Дата (позже)',
        lookup_expr='gt',
        widget = DateInput(
            attrs={
                'type': 'date'
            }
        ),
    )

    title = CharFilter(
        field_name='title',
        label='Название',
        lookup_expr='icontains',
    )

    author = CharFilter(
        field_name='author__user__username',
        label='Автор',
        lookup_expr='icontains'
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'date'
        ]