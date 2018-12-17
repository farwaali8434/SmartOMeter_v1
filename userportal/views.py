from django.contrib.auth.models import User, Group
from rest_framework import viewsets


from userportal.models import City, Area, Ticket, Invoice, Message
from userportal.models import Consumption, Announcement, Profile, Subscription, Meter
from userportal.serializers import UserSerializer, GroupSerializer, CitySerializer, ProfileSerializer
from userportal.serializers import MeterSerializer, AnnouncementSerializer, InvoiceSerializer, MessageSerializer
from userportal.serializers import TicketSerializer, ConsumptionSerializer, AreaSerializer, SubscriptionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer


class AreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MeterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Meter.objects.all()
    serializer_class = MeterSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer


class ConsumptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Consumption.objects.all()
    serializer_class = ConsumptionSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
