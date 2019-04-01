from django.urls import path, include, re_path

from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', profile, name='profile'),
    path('chat/', index1, name='index1'),
    re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]
