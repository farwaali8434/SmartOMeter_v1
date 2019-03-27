import datetime

from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import render
import stripe

from SmartOMeter_v1 import settings
from load_forecaster.LoadForecaster import Forecaster
from userportal.helpers import *
from userportal import models
from userportal import serializers


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer


class ConsumptionPagination(PageNumberPagination):
    page_size = 744


class ConsumptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Consumption.objects.all()
    serializer_class = serializers.ConsumptionSerializer
    pagination_class = ConsumptionPagination

    class meta:
        ordering = ['time_stamp']

    def get_queryset(self):
        today = datetime.datetime.now().date()
        return models.Consumption.objects.filter(meter__profile__user=self.request.user,
                                                 time_stamp__month=today.month,
                                                 time_stamp__year=today.year)


class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer

    def get_queryset(self):
        return self.request.user.ticket_set.all()


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer

    def get_queryset(self):
        area = self.request.user.profile.area
        return models.Announcement.objects.filter(area=area)


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentsAPI(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        token = request.data['stripe_token']
        try:
            stripe.Charge.create(
                amount=13000,
                currency='PKR',
                description='random',
                card=token
            )
        except stripe.error.CardError as e:
            body = e.json_body
            Response({'errors': body.get('error', {})}, status=400)
        return Response({"status": "complete"}, status=200)


# forecaster = Forecaster('load_forecaster/checkpoint/forecaster.h5')
@login_required
def dashboard(request):
    context = {
        'username': 'wadood',
        'year': consumption_sum(2018),
        'open_tickets': tickets(status=['O'])
    }
    return render(request, "dashboard.html", context)


@login_required
def profile(request):
    context = {
        'username': 'wadood'
    }
    return render(request, "registration/profile.html", context)
