import sqlite3
import json

include = ["userportal", "user", "token"]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def sql_table_names(connection):
    cursor = connection.cursor()
    cursor.execute("select name from sqlite_master where type = 'table';")
    tables = cursor.fetchall()
    cursor.close()
    return [table[0] for table in tables]


def load_sql_data(tables):
    data = {}
    connection.row_factory = dict_factory
    cursor = connection.cursor()

    for table in tables:
        if not any(ok in table for ok in include):
            continue
        cursor.execute(f"select * from {table};")
        data[table] = cursor.fetchall()

    cursor.close()
    return data


connection = sqlite3.connect("db.sqlite3")


if "__main__":
    tables = sql_table_names(connection)
    print(json.dumps(load_sql_data(tables)))
