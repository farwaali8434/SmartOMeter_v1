import datetime

from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, generics
from rest_framework.decorators import action
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

    class Meta:
        ordering = ['time_stamp']

    def get_queryset(self):
        today = datetime.datetime.now().date()
        return models.Consumption.objects.filter(meter__profile__user=self.request.user,
                                                 time_stamp__month=today.month,
                                                 time_stamp__year=today.year)

    day_labels = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    hour_labels = [("h" + str(i)) for i in range(24)]
    month_labels = [("m" + str(i)) for i in range(1, 12 + 1)]
    input_columns = {'MON': [], 'TUE': [], 'WED': [], 'THU': [], 'FRI': [], 'SAT': [], 'SUN': [],
                     'h0': [], 'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': [], 'h7': [], 'h8': [], 'h9': [], 'h10': [], 'h11': [],
                     'h12': [], 'h13': [], 'h14': [], 'h15': [], 'h16': [], 'h17': [], 'h18': [], 'h19': [], 'h20': [], 'h21': [], 'h22': [], 'h23': [],
                     'm1': [], 'm2': [], 'm3': [], 'm4': [], 'm5': [], 'm6': [], 'm7': [], 'm8': [], 'm9': [], 'm10': [], 'm11': [], 'm12': [],
                     'temp_n': [], 'temp_n^2': [], 'years_n': [], 'load_prev_n': []}

    @action(methods=['get'], detail=False)
    def predictions(self, request, *args, **kwargs):
        past_consumptions = [c for c in self.get_queryset()]
        today = datetime.datetime.now()
        future_inputs = Temperary.objects.filter(time_stamp__month=today.month,
                                                 time_stamp__gt=past_consumptions[-1].time_stamp)
        future_tensors = self.input_columns.copy()
        for fi in future_inputs:
            for index, week_day in enumerate(self.day_labels):
                future_tensors[week_day].append(1 if fi.time_stamp.weekday() == index else 0)

            for index, mon in enumerate(self.month_labels, 1):
                future_tensors[mon].append(1 if fi.month == index else 0)

            for index, hour in enumerate(self.hour_labels):
                future_tensors[hour].append(1 if fi.hour == index else 0)

            future_tensors['temp_n'].append(fi.temp_n)
            future_tensors['temp_n^2'].append(fi.temp_nn)
            future_tensors['years_n'].append(fi.year_n)
            future_tensors['load_prev_n'].append(fi.load_prev_n)

        page = self.paginate_queryset(past_consumptions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(past_consumptions, many=True)
        return Response(serializer.data)


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
