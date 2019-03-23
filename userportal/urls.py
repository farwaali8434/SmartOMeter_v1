from django.urls import path, re_path
from .views import index1, room
from . import views
app_name='chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', index1, name='index1'),
    re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]
