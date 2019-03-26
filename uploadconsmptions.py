from datetime import datetime

import pandas as pd
import sqlite3

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
    today = datetime.today()
    for index, row in data.iterrows():
        if row['time_stamp'] > today or row['time_stamp'].year != 2019:
            continue
        values = f"'{row['time_stamp']}', {2}, {row['load']}, {row['tempc']}"
        query = f'INSERT INTO userportal_consumption (time_stamp, meter_id, units, temperature) VALUES ({values})'
        cursor.execute(query)

    cursor.close()

    connection.commit()
    connection.close()
