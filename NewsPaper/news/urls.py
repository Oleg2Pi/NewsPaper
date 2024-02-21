from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    PostsList, PostDetail, PostsSearch, 
    NewsCreate, NewsUpdate, NewsDelete, 
    CategoryList, CategoryDetail, upgrade_me, subscribe
)


app_name = 'news'

urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', NewsCreate.as_view(), name='article_create'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('category/<int:pk>/subscribe/', subscribe, name='subscribe')
]