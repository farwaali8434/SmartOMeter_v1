from django.db.models import Sum
from django.db.models.functions import TruncMonth

from userportal.models import Consumption, Invoice, Subscription


def consumption_sum(year):
    consumptions = Consumption.objects.filter(time_stamp__year=year)
    year_sum = {'sum': 0}
    for c in consumptions:
        load = c.units
        month = c.time_stamp.month
        day = c.time_stamp.day
        hour = c.time_stamp.hour

        year_sum['sum'] += load

        if month not in year_sum:
            year_sum[month] = {'sum': 0}

        year_sum[month]['sum'] += load

        if day not in year_sum[month]:
            year_sum[month][day] = {'sum': 0}

        year_sum[month][day]['sum'] += load

        if hour not in year_sum[month][day]:
            year_sum[month][day][hour] = {'sum': 0}

        year_sum[month][day][hour]['sum'] += load

    return year_sum


def make_invoices(user_id):
    month_unit = (Consumption.objects.filter(meter__profile__user_id=user_id)
                                     .annotate(month=TruncMonth('time_stamp'))
                                     .values('month')
                                     .annotate(c=Sum('units')).order_by())
    rate = Subscription.objects.filter(profile__user_id=user_id)[0].rates
    [Invoice(month=aggregate['month'].month, month_units=aggregate['units']/100,
             amount=aggregate['units']*rate/100, user_id=user_id)
     for aggregate in month_unit]


make_invoices(2)