from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    # sentBy = models.CharField(max_length=50)
    detail = models.TextField(max_length=100)


class Ticket(models.Model):
    status = models.CharField(max_length=10)
    dateOpened = models.DateField(auto_now_add=True)
    dateClosed = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)


class Invoice(models.Model):
    month = models.CharField(max_length=10)
    amount = models.IntegerField(max_length=10)


class Subscription(models.Model):
    type = models.CharField(max_length=4)
    rates = models.PositiveIntegerField(max_length=5)


class Consumption(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    units = models.PositiveIntegerField(max_length=5)


class Area(models.Model):
    areaName = models.TextField()
    city = models.CharField(max_length=15)
    zone = models.CharField(max_length=15)
    # block = models.CharField(5)
    # areaId = models.CharField(20)


class Announcement(models.Model):
    effectiveFrom = models.TimeField()
    effectiveTill = models.TimeField()
    subject = models.CharField(max_length=50)
    detail = models.CharField(max_length=100)


class Meter(models.Model):
    address = models.CharField(max_length=50)
    meterNum = models.IntegerField(max_length=20)
    # Area


class City(models.Model):
    postalCode = models.PositiveIntegerField(max_length=5)
    cityName = models.CharField(max_length=20)






