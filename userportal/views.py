import datetime
import json
import pandas as pd

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, F, IntegerField, Sum, DecimalField, Value
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models.functions import Extract
import stripe
from django.shortcuts import render
from SmartOMeter_v1 import settings
from load_forecaster.LoadForecaster import Forecaster
from userportal.helpers import *
from userportal import models
from userportal import serializers
from django.utils.safestring import mark_safe


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer

    def get_queryset(self):
        return models.Invoice.objects.filter(user=self.request.user)


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
                     'h0': [], 'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': [], 'h7': [], 'h8': [], 'h9': [],
                     'h10': [], 'h11': [],
                     'h12': [], 'h13': [], 'h14': [], 'h15': [], 'h16': [], 'h17': [], 'h18': [], 'h19': [], 'h20': [],
                     'h21': [], 'h22': [], 'h23': [],
                     'm1': [], 'm2': [], 'm3': [], 'm4': [], 'm5': [], 'm6': [], 'm7': [], 'm8': [], 'm9': [],
                     'm10': [], 'm11': [], 'm12': [],
                     'temp_n': [], 'temp_n^2': [], 'years_n': [], 'load_prev_n': []}

    @action(methods=['get'], detail=False)
    def predictions(self, request):
        past_consumptions = [c for c in self.get_queryset()]
        forecaster = Forecaster('load_forecaster/checkpoint/forecaster.h5')
        today = datetime.datetime.now()
        future_inputs = Temperary.objects.filter(time_stamp__month=today.month,
                                                 time_stamp__gt=past_consumptions[-1].time_stamp)
        future_tensors = self.input_columns.copy()

        for fi in future_inputs:
            for index, week_day in enumerate(self.day_labels):
                future_tensors[week_day].append(1 if fi.time_stamp.weekday() == index else 0)

            for index, mon in enumerate(self.month_labels, 1):
                future_tensors[mon].append(1 if fi.time_stamp.month == index else 0)

            for index, hour in enumerate(self.hour_labels):
                future_tensors[hour].append(1 if fi.time_stamp.hour == index else 0)

            future_tensors['temp_n'].append(fi.temp_n)
            future_tensors['temp_n^2'].append(fi.temp_nn)
            future_tensors['years_n'].append(fi.years_n)
            future_tensors['load_prev_n'].append(fi.load_prev_n)
        predictions = forecaster.predict(pd.DataFrame(future_tensors))
        past_consumptions += [Consumption(id=0, time_stamp=fi.time_stamp, units=output,
                                          meter_id=past_consumptions[-1].meter_id, temperature=25)
                              for fi, output in zip(future_inputs, predictions)]

        page = self.paginate_queryset(past_consumptions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(past_consumptions, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def summarize(self, request):
        today = datetime.datetime.now()
        span = request.query_params['span']
        span_id = request.query_params['span_id']
        month = request.query_params.get('month')

        if month:
            period = 'day'
            query_set = models.Consumption.objects.filter(
                time_stamp__year=today.year,
                time_stamp__month=month
            )
        else:
            period = 'month'
            query_set = models.Consumption.objects.filter(
                time_stamp__year=today.year
            )

        if span == 'city':
            query_set = query_set.filter(meter__area__city_id=span_id)
        elif span == 'area':
            query_set = query_set.filter(meter__area_id=span_id)

        summary = list(
            query_set.annotate(**{
                period: Extract('time_stamp', period)
            }).values(period).annotate(load=Sum('units'))
        )
        return Response(summary)

    @action(methods=['GET'], detail=False)
    def compare(self, request):
        today = datetime.datetime.now()
        span = request.query_params['span']
        span_ids = [int(x) for x in request.query_params['span_ids'].split(',') if x != '']
        months = [int(x) for x in request.query_params['months'].split(',') if x != '']

        if months:
            query_set = models.Consumption.objects.filter(
                time_stamp__year=today.year,
                time_stamp__month__in=months
            )
        else:
            query_set = models.Consumption.objects.filter(
                time_stamp__year=today.year
            )

        if span == 'city':
            query_set = query_set.filter(meter__area__city_id__in=span_ids)
        elif span == 'area':
            query_set = query_set.filter(meter__area_id__in=span_ids)

        comparison = list(query_set.annotate(
            span=F(f'meter__area{"__city__city_name" if span == "city" else "__area_name"}')
        ).values('span').annotate(load=Sum('units')))
        return Response(comparison)


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
        invoice_id = request.data['invoiceId']
        invoice = Invoice.objects.filter(id=invoice_id)[0]
        try:
            stripe.Charge.create(
                amount=int(invoice.amount),
                currency='PKR',
                description=invoice.issue_date,
                card=token
            )
        except stripe.error.CardError as e:
            body = e.json_body
            return Response({'errors': body.get('error', {})}, status=400)
        invoice.paid = True
        invoice.save()
        return Response({"status": "complete"}, status=200)


@login_required
def dashboard(request):
    serializer = CityContextSerializer(City.objects.all(), many=True)
    context = {
        'username': request.user.username,
        'open_tickets_count': tickets(['O'], True),
        'json_conifg': json.dumps(serializer.data)
    }
    return render(request, "dashboard.html", context)


@login_required
def profile(request):
    context = {
        'username': request.user.username
    }
    return render(request, "registration/profile.html", context)


def index(request):
    return render(request, 'userportal/index.html', {})


@login_required
def room(request, room_name):
    return render(request, 'userportal/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket