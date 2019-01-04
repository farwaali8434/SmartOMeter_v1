from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
ID_LENGTH = 15
DEFAULT_RATE = 10
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

    def __str__(self):
        return self.title


class Message(models.Model):
    # subject = models.CharField(max_length=MEDIUM_LENGTH)
    created = models.DateTimeField(auto_now_add=True)
    detail = models.TextField(max_length=LONG_LENGTH)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class City(models.Model):
    postal_code = models.PositiveIntegerField(max_length=5)
    city_name = models.CharField(max_length=SHORT_LENGTH)

    def __str__(self):
        return self.city_name


class Area(models.Model):
    area_name = models.CharField(max_length=SHORT_LENGTH)
    division = models.CharField(max_length=SHORT_LENGTH)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.area_name


class Meter(models.Model):
    street = models.CharField(max_length=MEDIUM_LENGTH)
    meter_num = models.IntegerField(max_length=ID_LENGTH)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.meter_num)


class Invoice(models.Model):
    month = models.CharField(max_length=SHORT_LENGTH, choices=MONTHS)
    amount = models.FloatField(default=DEFAULT_BILL)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reading_date = models.DateField(auto_now=True)
    issue_date = models.DateField(auto_now=True)
    due_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.amount) + ' ' + self.month


class Subscription(models.Model):
    TYPES = [
        ('PRE', 'Prepaid'),
        ('POST', 'Postpaid')
    ]
    type = models.CharField(max_length=SHORT_LENGTH, choices=TYPES)
    rates = models.FloatField(default=DEFAULT_RATE)

    def __str__(self):
        return self.type


class Announcement(models.Model):
    effective_from = models.TimeField()
    effective_till = models.TimeField()
    subject = models.CharField(max_length=50)
    detail = models.CharField(max_length=100)
    areas = models.ManyToManyField(Area)

    def __str__(self):
        return self.subject


class Consumption(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    units = models.PositiveIntegerField(max_length=5)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.units)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnic = models.PositiveIntegerField(max_length=ID_LENGTH, null=True)
    phone_num = models.PositiveIntegerField(max_length=ID_LENGTH, null=True)
    street = models.CharField(max_length=MEDIUM_LENGTH, null=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



