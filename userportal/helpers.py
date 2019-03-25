from userportal.models import *
from userportal.serializers import *


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


def tickets(status=('O', 'E', 'C')):
    return [TicketSerializer(t).data for t in Ticket.objects.filter(status__in=status)]


