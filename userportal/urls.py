from django.urls import path, include, re_path

from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', profile, name='profile'),
    path('invoice/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice/<int:id>', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('chat/', index, name='index1'),
    re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]
