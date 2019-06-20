from django.urls import path, include, re_path

from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', profile, name='profile'),
    path('invoice/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice/<int:pk>', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('ticket/', TicketListView.as_view(), name='ticket_list'),
    path('ticket/<int:pk>', TicketDetailView.as_view(), name='ticket_detail'),
]
