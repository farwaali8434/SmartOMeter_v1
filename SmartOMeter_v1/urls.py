"""SmartOMeter_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from userportal import views
from .views import login

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'areas', views.AreaViewSet)
router.register(r'tickets', views.TicketViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'meters', views.MeterViewSet)
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'subscriptions', views.SubscriptionViewSet)
router.register(r'announcements', views.AnnouncementViewSet)
router.register(r'consumptions', views.ConsumptionViewSet)
router.register(r'profile', views.ProfileViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    path('userdata/', views.UsersDetailView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/login', login)
]
