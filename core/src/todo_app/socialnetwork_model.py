from datetime import date
import os
from peewee import *
import peewee
from loguru import logger

db = SqliteDatabase('twitter.db')
#db.execute_sql('PRAGMA foreign_keys = ON;')
class UsersTable(Model):
    user_id = CharField(unique=True, max_length=30)
    user_name = CharField(max_length=30)
    user_last_name = CharField(max_length=100)
    user_email = TextField()

    class Meta:
        database = db  # This model uses the "twitter.db" database.
        constraints = [peewee.Check("LENGTH(user_id) < 30"),
                        peewee.Check("LENGTH(user_name) < 30"),
                        peewee.Check("LENGTH(user_last_name) < 100")]

class StatusTable(Model):
    status_id = CharField(unique=True)
    user_id = ForeignKeyField(UsersTable, to_field='user_id', backref='statuses', on_delete='CASCADE')
    status_text = TextField()

    class Meta:
        database = db  # this model uses the "twitter.db" database

def create_tables(database):
    database.create_tables([UsersTable, StatusTable])

# #https://www.fullstackpython.com/blog/export-pandas-dataframes-sqlite-sqlalchemy.html
# import os
# from pandas import read_csv
# from sqlalchemy import create_engine

# try:
#     os.remove("twitter.db")
# except:
#     pass

# status_table = read_csv("status_updates.csv", encoding="utf-8")
# users_table = read_csv("accounts.csv", encoding="utf-8")

# engine = create_engine('sqlite:///twitter.db', echo=True)
# sqlite_connection = engine.connect()

# users_table.to_sql("users_table", sqlite_connection, if_exists='fail')
# status_table.to_sql("status_table", sqlite_connection, if_exists='fail')


# execute = sqlite_connection.execute("SELECT user_id FROM users_table LIMIT 10")

# result = sorted([row[0] for row in execute])
# print(result)