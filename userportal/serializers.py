from django.contrib.auth.models import User, Group
from rest_framework import serializers

from userportal.models import City, Area, Ticket, Consumption, Invoice
from userportal.models import Meter, Profile, Subscription, Announcement, Message


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('postal_code', 'city_name')


class AreaSerializer(serializers.HyperlinkedModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Area
        fields = ('area_name', 'division', 'city')


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subscription
        fields = ('type', 'rates')


class MeterSerializer(serializers.HyperlinkedModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = Meter
        fields = ('meter_num', 'street', 'area', )


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    meter = MeterSerializer()
    subscription = SubscriptionSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'cnic', 'phone_num', 'street', 'meter', 'subscription')


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Ticket
        fields = ('status', 'title', 'date_opened', 'date_closed', 'user')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    ticket = TicketSerializer()

    class Meta:
        model = Message
        fields = ('created', 'detail', 'ticket')


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Invoice
        fields = ('month', 'amount', 'reading_date', 'issue_date', 'due_date', 'paid', 'user')


class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = Announcement
        fields = ('subject', 'detail', 'effective_from', 'effective_till', 'area')


class ConsumptionSerializer(serializers.HyperlinkedModelSerializer):
    meter = MeterSerializer()

    class Meta:
        model = Consumption
        fields = ('units', 'time_stamp', 'meter')


