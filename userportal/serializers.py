from django.contrib.auth.models import User, Group
from rest_framework import serializers

from userportal.models import City, Area, Ticket, Consumption, Invoice
from userportal.models import Meter, Profile, Subscription, Announcement, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


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


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('detail', 'sent_by', 'ticket', 'sent')
        read_only_fields = ('ticket', 'sent_by')


class TicketSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, partial=True)

    def create(self, validated_data):
        validated_data.update({'created_by': self.context['request'].user})
        messages = validated_data.pop('messages')
        ticket = Ticket.objects.create(**validated_data)
        for message in messages:
            message.update({'sent_by': self.context['request'].user})
            Message.objects.create(**message, ticket=ticket)
        return ticket
    #
    # def update(self, ticket, validated_data):
    #     messages = validated_data.pop('messages')
    #     ticket.title = validated_data.get('title', ticket.title)
    #     ticket.status = validated_data.get('title', ticket.status)
    #     ticket.date_closed = validated_data.get('date_closed', ticket.date_closed)
    #     ticket.save()
    #     keep_messages =

    class Meta:
        model = Ticket
        fields = ('id', 'subject', 'status', 'date_opened', 'date_closed', 'created_by', 'messages')
        read_only_fields = ('created_by',)


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Invoice
        fields = ('month', 'amount', 'reading_date', 'issue_date', 'due_date', 'paid', 'user')


class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = ('id', 'subject', 'detail', 'effective_from', 'effective_till', 'area')


class ConsumptionSerializer(serializers.HyperlinkedModelSerializer):
    meter = MeterSerializer()

    class Meta:
        model = Consumption
        fields = ('units', 'time_stamp', 'meter')


