from datetime import datetime

import pandas as pd
import sqlite3

connection = sqlite3.connect("db.sqlite3")


if "__main__":
    cursor = connection.cursor()
    data = pd.read_csv('load_forecaster/data/SCENT.csv')
    data['time_stamp'] = data.apply(lambda x: datetime(
        int(x['year']),
        int(x['month']),
        int(x['day']),
        int(x['hour'])),
        axis=1)
    for index, row in data.iterrows():
        values = f"'{row['time_stamp']}', {2}, {row['load']}, {row['tempc']}"
        query = f'INSERT INTO userportal_consumption (time_stamp, meter_id, units, temperature) VALUES ({values})'
        cursor.execute(query)
    cursor.close()

    connection.commit()
    connection.close()
