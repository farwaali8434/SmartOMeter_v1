from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

DEFAULT_BILL = 300
LONG_LENGTH = 500
MEDIUM_LENGTH = 200
SHORT_LENGTH = 50
MONTHS = (
    ('JAN', 'January'),
    ('FEB', 'February'),
    ('MAR', 'March'),
    ('APR', 'April'),
    ('MAY', 'May'),
    ('JUN', 'June'),
    ('JUL', 'July'),
    ('AUG', 'August'),
    ('SEP', 'September'),
    ('OCT', 'October'),
    ('NOV', 'November'),
    ('DEC', 'December')
)


class Ticket(models.Model):
    STATUSES = (
        ('O', 'Opened'),
        ('E', 'Escalated'),
        ('C', 'Closed'),
    )
    title = models.CharField(max_length=MEDIUM_LENGTH)
    status = models.CharField(max_length=1, choices=STATUSES)
    date_opened = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    subject = models.CharField(max_length=MEDIUM_LENGTH)
    created = models.DateTimeField(auto_now_add=True)
    detail = models.TextField(max_length=LONG_LENGTH)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)


class Meter(models.Model):
    street = models.CharField(max_length=MEDIUM_LENGTH)
    meter_num = models.IntegerField(max_length=20)
    area = models.ForeignKey(Area)


class Invoice(models.Model):
    month = models.CharField(max_length=SHORT_LENGTH, choices=MONTHS)
    amount = models.FloatField(default=DEFAULT_BILL)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User)


class Subscription(models.Model):
    type = models.CharField(max_length=4)
    rates = models.PositiveIntegerField(max_length=5)


class Area(models.Model):
    area_name = models.TextField()
    city = models.CharField(max_length=15)
    zone = models.CharField(max_length=15)


class Announcement(models.Model):
    effective_from = models.TimeField()
    effective_till = models.TimeField()
    subject = models.CharField(max_length=50)
    detail = models.CharField(max_length=100)
    areas = models.ManyToManyField(Area)





class Consumption(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    units = models.PositiveIntegerField(max_length=5)
    meter = models.ForeignKey(Meter)


class City(models.Model):
    postal_code = models.PositiveIntegerField(max_length=5)
    city_name = models.CharField(max_length=20)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnic = models.PositiveIntegerField(max_length=15)
    phone_num = models.PositiveIntegerField(max_length=15)
    street_address = models.CharField(max_length=50)
    area = models.ForeignKey(Area)
    meter = models.ForeignKey(Meter)
    subscription = models.ForeignKey(Subscription)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
