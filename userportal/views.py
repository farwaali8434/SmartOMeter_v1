from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from userportal import models
from userportal import serializers


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
