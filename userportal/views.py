from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import stripe
from django.shortcuts import render
from SmartOMeter_v1 import settings
from userportal import models
from userportal import serializers
from django.utils.safestring import mark_safe
import json


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer


class ConsumptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Consumption.objects.all()
    serializer_class = serializers.ConsumptionSerializer
    permission_classes = [AllowAny]


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
    #
    # def get_queryset(self):
    #     area = self.request.user.profile.area
    #     return models.Announcement.objects.filter(area_)


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


def index(request):
    from django.shortcuts import render
    return render(request, "demandanalysis.html")


def index1(request):
    return render(request, 'userportal/index1.html', {})


def room(request, room_name):
    return render(request, 'userportal/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
