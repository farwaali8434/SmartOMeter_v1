from userportal.models import Consumption

consumptions = Consumption.objects.filter(time_stamp__year=2018)
year = {'sum': 0}
for c in consumptions:
    load = c.units
    month = c.time_stamp.month
    day = c.time_stamp.day
    hour = c.time_stamp.hour

    year['sum'] += load

    if month not in year:
        year[month] = {'sum': 0}

    year[month]['sum'] += load

    if day not in year[month]:
        year[month][day] = {'sum': 0}

    year[month][day]['sum'] += load

    if hour not in year[month][day]:
        year[month][day][hour] = {'sum': 0}

    year[month][day][hour]['sum'] += load

print(year)