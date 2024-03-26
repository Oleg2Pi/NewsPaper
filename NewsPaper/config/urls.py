from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from news.views import NewsViewset #ArticlesListViewset


router = routers.DefaultRouter()
router.register(r'news', NewsViewset)
# router.register(r'articles', ArticlesListViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls', namespace='news')),
    path('accounts/', include('allauth.urls')),
    # подключаем встроенные эндопинты для работы с локализацией
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
