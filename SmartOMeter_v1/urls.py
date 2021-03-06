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
from userportal.views import *
from .views import login, user


router = routers.DefaultRouter()

router.register(r'tickets', TicketViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'consumptions', ConsumptionViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/login', login),
    url(r'^api/user', user),
    url(r'^api/charge', PaymentsAPI.as_view()),
    path('', include('userportal.urls')),
]

# Permissions = {
#     "Create": ([Staff, Admin], False),
#     "Read": ([Consumer!, Staff*, Admin*], False),
#     "Update": ([Staff!, Admin*], False),
#     "Delete": ([Admin*], False)
# }
