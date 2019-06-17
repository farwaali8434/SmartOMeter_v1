from rest_framework import serializers

from userportal import models


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Invoice
        fields = ('id', 'month', 'amount', 'month_units', 'issue_date', 'due_date', 'paid')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ('postal_code', 'city_name')


class AreaSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = models.Area
        fields = ('area_name', 'division', 'city')


class MeterSerializer(serializers.ModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = models.Meter
        fields = ('meter_num', 'street', 'area', )


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subscription
        fields = ('type', 'rates')


class ProfileSerializer(serializers.ModelSerializer):
    meter = MeterSerializer()
    subscription = SubscriptionSerializer()
    invoices = InvoiceSerializer(many=True)

    class Meta:
        model = models.Profile
        fields = ('user', 'cnic', 'phone_num', 'street', 'meter', 'subscription', 'invoices')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = models.User
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'email', 'profile')


class MessageUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'username', 'first_name', 'last_name')


class MessageSerializer(serializers.ModelSerializer):
    sent_by = MessageUserSerializer()

    class Meta:
        model = models.Message
        fields = ('id', 'detail', 'sent_by', 'ticket', 'sent')
        read_only_fields = ('ticket', 'sent_by')


class TicketSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, partial=True)

    def create(self, validated_data):
        validated_data.update({'created_by': self.context['request'].user})
        messages = validated_data.pop('messages')
        ticket = models.Ticket.objects.create(**validated_data)
        for message in messages:
            message.update({'sent_by': self.context['request'].user})
            models.Message.objects.create(**message, ticket=ticket)
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
        model = models.Ticket
        fields = ('id', 'subject', 'status', 'date_opened', 'date_closed', 'created_by', 'messages')
        read_only_fields = ('created_by',)


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ('id', 'subject', 'detail', 'effective_from', 'effective_till', 'area')


class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Consumption
        fields = ('id', 'units', 'time_stamp', 'meter')


class MeterContextSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Meter
        fields = ('id', 'meter_num', 'street')


class AreaContextSerializer(serializers.ModelSerializer):
    meters = MeterContextSerializer(many=True)

    class Meta:
        model = models.Area
        fields = ('id', 'area_name', 'meters')


class CityContextSerializer(serializers.ModelSerializer):
    areas = AreaContextSerializer(many=True)

    class Meta:
        model = models.City
        fields = ('id', 'city_name', 'areas')
