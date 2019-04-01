from datetime import datetime

import numpy
import pandas as pd
import sqlite3
from scipy.stats import zscore


def add_noise(m, std):
    noise = numpy.random.normal(0, std, m.shape[0])
    return m + noise


connection = sqlite3.connect("db.sqlite3")


if "__main__":
    cursor = connection.cursor()
    data = pd.read_csv('load_forecaster/data/SCENT.csv')
    next_year = []
    for row in data['year']:
        next_year.append(row+1 if row == 2018 else row)
    data['year'] = next_year

    data['time_stamp'] = data.apply(lambda x: datetime(
        int(x['year']),
        int(x['month']),
        int(x['day']),
        int(x['hour'])),
        axis=1)

    temperature = data["tempc"].replace([-9999], numpy.nan)
    temperature.ffill(inplace=True)
    temperature_predictions = add_noise(temperature, std=2.5)
    data["temp_n"] = zscore(temperature_predictions)
    data['temp_n^2'] = data["temp_n"] ** 2

    data["load_n"] = zscore(data["load"])
    data["load_prev_n"] = data["load_n"].shift(24)
    data["load_prev_n"].bfill(inplace=True)
    data["years_n"] = zscore(data["year"])

    today = datetime.today()
    for index, row in data.iterrows():
        if row['time_stamp'].year == 2019:
            values2 = f"'{row['time_stamp']}', {row['temp_n']}, {row['temp_n^2']}, {row['load_prev_n']}, {row['years_n']}"
            query2 = f'INSERT INTO userportal_temperary (time_stamp, temp_n, temp_nn, load_prev_n, years_n) VALUES ({values2})'
            cursor.execute(query2)

            if row['time_stamp'] > today:
                continue
            values = f"'{row['time_stamp']}', {2}, {row['load']}, {row['tempc']}"
            query = f'INSERT INTO userportal_consumption (time_stamp, meter_id, units, temperature) VALUES ({values})'
            # cursor.execute(query)

    cursor.close()
    connection.commit()
    connection.close()
