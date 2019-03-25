from django.urls import path, include

from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', profile, name='profile'),
]
