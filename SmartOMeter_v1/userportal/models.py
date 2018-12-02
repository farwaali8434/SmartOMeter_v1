from django.db import models


class Ticket(models.Model):
    status = models.CharField(max_length=10)
    date_opened = models.DateField(auto_now_add=True)
    date_closed = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)


class Message(models.Model):
    subject = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    # sentBy = models.CharField(max_length=50)
    detail = models.TextField(max_length=100)
    ticket = models.ForeignKey(Ticket)


class Invoice(models.Model):
    month = models.CharField(max_length=10)
    amount = models.IntegerField(max_length=10)


class Subscription(models.Model):
    type = models.CharField(max_length=4)
    rates = models.PositiveIntegerField(max_length=5)


class Area(models.Model):
    area_name = models.TextField()
    city = models.CharField(max_length=15)
    zone = models.CharField(max_length=15)
    # block = models.CharField(5)
    # areaId = models.CharField(20)


class Announcement(models.Model):
    effective_from = models.TimeField()
    effective_till = models.TimeField()
    subject = models.CharField(max_length=50)
    detail = models.CharField(max_length=100)
    areas = models.ManyToManyField(Area)


class Meter(models.Model):
    address = models.CharField(max_length=50)
    meter_num = models.IntegerField(max_length=20)
    area = models.ForeignKey(Area)


class Consumption(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    units = models.PositiveIntegerField(max_length=5)
    meter = models.ForeignKey(Meter)


class City(models.Model):
    postal_code = models.PositiveIntegerField(max_length=5)
    city_name = models.CharField(max_length=20)


class User(models.Model):
    cnic = models.PositiveIntegerField(max_length=15)
    phone_num = models.PositiveIntegerField(max_length=15)
    street_add = models.CharField(max_length=50)
    area = models.ForeignKey(Area)
    meter = models.ForeignKey(Meter)
    invoice = models.ForeignKey(Invoice)
    subscription = models.ForeignKey(Subscription)



