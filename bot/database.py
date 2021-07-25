"""
This file manages database requests and connections
"""

import logging

from peewee import *

from config import database_name

# Only for developing
# TODO: switch to postgresql
database = SqliteDatabase(database_name)
database.connect()

logging.info("Database connection established")


class BaseModel(Model):
    class Meta:
        database = database
        only_save_dirty = True


class User(BaseModel):
    tg_id = IntegerField(unique=True)
    name = CharField()


class BaseTask(BaseModel):
    name = CharField()
    description = TextField()
    user = ForeignKeyField(User, backref="meetings")


class Meeting(BaseTask):
    date = DateTimeField()


class Task(BaseTask):
    status = CharField()


database.create_tables([User, Meeting, Task])

logging.info("Database tables created successfully")
