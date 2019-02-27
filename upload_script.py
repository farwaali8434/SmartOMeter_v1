import sqlite3
DATA = {
  "auth_user_groups": [],
  "auth_user_user_permissions": [],
  "auth_user": [
    {
      "id": 2,
      "password": "pbkdf2_sha256$120000$YPBZSzucEcNI$OfnkP2t8RV+IUOo3fT6ORE7PW/XayUoAam/+Kq6Lhvg=",
      "last_login": "None",
      "is_superuser": 0,
      "username": "testuser1",
      "first_name": "Test1",
      "email": "testuser1@abc.com",
      "is_staff": 0,
      "is_active": 1,
      "date_joined": "2019-02-27 13:58:04",
      "last_name": "User1"
    },
    {
      "id": 3,
      "password": "pbkdf2_sha256$120000$alpQ85vloG2t$rfO4Pr3qFtBudVKVUGxNhs6ktXqdryt5YvsoG7PgXP4=",
      "last_login": "None",
      "is_superuser": 0,
      "username": "testuser2",
      "first_name": "Test2",
      "email": "testuser2@abc.com",
      "is_staff": 0,
      "is_active": 1,
      "date_joined": "2019-02-27 14:00:36",
      "last_name": "User2"
    },
    {
      "id": 4,
      "password": "pbkdf2_sha256$120000$rivRheljY3fo$FKNQLwZ4nSLH+MSTvVZJSlASbvsJSgkkGg2DKm6xliU=",
      "last_login": "None",
      "is_superuser": 0,
      "username": "testuser3",
      "first_name": "Test3",
      "email": "testuser3@abc.com",
      "is_staff": 0,
      "is_active": 1,
      "date_joined": "2019-02-27 14:01:32",
      "last_name": "User3"
    },
    {
      "id": 5,
      "password": "pbkdf2_sha256$120000$0TUlwjKM5DRw$oFfRAe0n/Ot1IfL9ZFihahVcuX8RTm8CCXoaAEx25w4=",
      "last_login": "None",
      "is_superuser": 0,
      "username": "testuser4",
      "first_name": "Test4",
      "email": "testuser4@abc.com",
      "is_staff": 0,
      "is_active": 1,
      "date_joined": "2019-02-27 14:02:30",
      "last_name": "User4"
    },
    {
      "id": 6,
      "password": "pbkdf2_sha256$120000$4baA98H5fZ9f$LgNm8gvIab/ER0fH7meWmxa2nALFhiQV8xVeZgmOmFo=",
      "last_login": "None",
      "is_superuser": 0,
      "username": "testuser5",
      "first_name": "Test5",
      "email": "testuser5@abc.com",
      "is_staff": 0,
      "is_active": 1,
      "date_joined": "2019-02-27 14:04:46",
      "last_name": "User5"
    },
    {
      "id": 7,
      "password": "pbkdf2_sha256$120000$butZU7ptxjjU$QIQeD6sS0bn5RAxFGxxz2KcLnFUeSDZolr2qNmRaa0E=",
      "last_login": "None",
      "is_superuser": 0,
      "username": "inactiveuser",
      "first_name": "Inactive",
      "email": "inactiveuser@abc.com",
      "is_staff": 0,
      "is_active": 0,
      "date_joined": "2019-02-27 14:37:32",
      "last_name": "User"
    }
  ],
  "authtoken_token": [
    {
      "key": "59634c196f1be3389f4718c20b137d22d6c248b7",
      "created": "2019-02-27 14:12:04.287447",
      "user_id": 2
    },
    {
      "key": "605610d96578725e87e7b9ef368eed84e7e1532b",
      "created": "2019-02-27 14:12:17.227941",
      "user_id": 3
    },
    {
      "key": "e3700df4270177108e352a65f03cca4c58a8b551",
      "created": "2019-02-27 14:12:46.264350",
      "user_id": 4
    },
    {
      "key": "bb906be36aceb7a477f922409e2ddd8b569bb02b",
      "created": "2019-02-27 14:12:53.339308",
      "user_id": 5
    },
    {
      "key": "74c73036ad0e4af0d10115c261c8f58ed2f78d27",
      "created": "2019-02-27 14:39:50.766151",
      "user_id": 7
    }
  ],
  "userportal_announcement": [
    {
      "id": 1,
      "effective_from": "12:43:36",
      "effective_till": "14:43:28",
      "subject": "Schedualed Shutdown",
      "detail": "We are going to shutdown the power for your area for the mentioned duration. Sorry for inconvenience"
    },
    {
      "id": 2,
      "effective_from": "02:43:54",
      "effective_till": "04:43:58",
      "subject": "Schedualed Shutdown2",
      "detail": "We are going to Increase the power for your area for the mentioned duration. Sorry for inconvenience"
    }
  ],
  "userportal_city": [
    {
      "id": 1,
      "postal_code": 35400,
      "city_name": "Chiniot"
    },
    {
      "id": 2,
      "postal_code": 38000,
      "city_name": "Faisalabad"
    },
    {
      "id": 3,
      "postal_code": 54000,
      "city_name": "Lahore"
    },
    {
      "id": 4,
      "postal_code": 46000,
      "city_name": "Rawalpindi"
    },
    {
      "id": 5,
      "postal_code": 74200,
      "city_name": "Karachi"
    }
  ],
  "userportal_invoice": [],
  "userportal_meter": [
    {
      "id": 1,
      "street": "P #1, Dilshah Colony, Dummy Town",
      "meter_num": 111,
      "area_id": 3
    },
    {
      "id": 2,
      "street": "P #33, Peoples Colony, Dummy Town",
      "meter_num": 222,
      "area_id": 5
    }
  ],
  "userportal_subscription": [
    {
      "id": 1,
      "type": "PRE",
      "rates": 10
    },
    {
      "id": 2,
      "type": "POST",
      "rates": 12
    }
  ],
  "userportal_ticket": [],
  "userportal_profile": [
    {
      "id": 2,
      "cnic": 12345678901,
      "phone_num": 3009658434,
      "street": "P #1, Dilshah Colony, Dummy Town",
      "area_id": 3,
      "meter_id": 1,
      "subscription_id": 1,
      "user_id": 2
    },
    {
      "id": 3,
      "cnic": 3210043909539,
      "phone_num": 3219558434,
      "street": "P #33, Peoples Colony, Dummy Town",
      "area_id": 5,
      "meter_id": 2,
      "subscription_id": 2,
      "user_id": 3
    },
    {
      "id": 4,
      "cnic": "None",
      "phone_num": "None",
      "street": "None",
      "area_id": "None",
      "meter_id": "None",
      "subscription_id": "None",
      "user_id": 4
    },
    {
      "id": 5,
      "cnic": "None",
      "phone_num": "None",
      "street": "None",
      "area_id": "None",
      "meter_id": "None",
      "subscription_id": "None",
      "user_id": 5
    },
    {
      "id": 6,
      "cnic": "None",
      "phone_num": "None",
      "street": "None",
      "area_id": "None",
      "meter_id": "None",
      "subscription_id": "None",
      "user_id": 6
    },
    {
      "id": 7,
      "cnic": "None",
      "phone_num": "None",
      "street": "None",
      "area_id": "None",
      "meter_id": "None",
      "subscription_id": "None",
      "user_id": 7
    }
  ],
  "userportal_message": [],
  "userportal_consumption": [],
  "userportal_area": [
    {
      "id": 1,
      "area_name": "Karachi GPO",
      "division": "Karachi",
      "city_id": 5
    },
    {
      "id": 2,
      "area_name": "Islamabad GPO",
      "division": "Islamabad",
      "city_id": 4
    },
    {
      "id": 3,
      "area_name": "Muslim Town",
      "division": "Faisalabad",
      "city_id": 2
    },
    {
      "id": 4,
      "area_name": "Iqbal Town",
      "division": "Lahore",
      "city_id": 3
    },
    {
      "id": 5,
      "area_name": "WAPDA Town",
      "division": "Lahore",
      "city_id": 3
    }
  ],
  "userportal_announcement_area": [
    {
      "id": 1,
      "announcement_id": 1,
      "area_id": 3
    },
    {
      "id": 2,
      "announcement_id": 2,
      "area_id": 3
    },
    {
      "id": 3,
      "announcement_id": 2,
      "area_id": 5
    }
  ]
}


connection = sqlite3.connect("db.sqlite3")


def upload(tables):
    cursor = connection.cursor()

    for table, data in tables.items():
        for row in data:
            columns = ",".join(row.keys())
            values = ",".join([str(v) if isinstance(v, int) else f'"{v}"' for v in row.values()])
            query = f'INSERT INTO {table} ({columns}) VALUES ({values})'
            cursor.execute(query)

    cursor.close()


if "__main__":
    upload(DATA)
    connection.commit()
    connection.close()
