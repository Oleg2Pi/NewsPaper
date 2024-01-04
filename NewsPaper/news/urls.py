from django.urls import path
from .views import (
    PostsList, PostDetail, PostsSearch, NewsCreate, NewsUpdate, NewsDelete,
)


urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:id>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', NewsCreate.as_view(), name='article_create'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
]