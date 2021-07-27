"""
This file manages database requests and connections
"""

import logging

from peewee import *

from bot.config import database_name

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

    @staticmethod
    def is_user_exists(tg_id: int) -> bool:
        return User.get_or_none(User.tg_id == tg_id) is not None


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
logging.info("Database is ready for using")
