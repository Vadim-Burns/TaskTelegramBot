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

    @staticmethod
    def get_by_tg_id(tg_id: int) -> 'User':
        return User.get(User.tg_id == tg_id)

    @staticmethod
    def delete_cascade(tg_id: int):
        user = User.get(User.tg_id == tg_id)

        Meeting.delete().where(Meeting.user == user).execute()
        Task.delete().where(Task.user == user).execute()
        user.delete_instance()


class BaseTask(BaseModel):
    name = CharField()
    description = TextField()


class Meeting(BaseTask):
    date = DateTimeField()
    user = ForeignKeyField(User, backref="meetings")

    @staticmethod
    def get_by_user(user: User) -> 'list of Meeting':
        return Meeting.select().where(Meeting.user == user).execute()

    def to_beauty_str(self) -> str:
        return "Meeting info:\nName - {name}\nDescription - {description}\nDate - {date}".format(
            name=self.name,
            description=self.description,
            date=self.date
        )


class Task(BaseTask):
    status = CharField(default="not started")
    user = ForeignKeyField(User, backref="tasks")

    @staticmethod
    def get_by_user(user: User) -> 'list of Task':
        return Task.select().where(Task.user == user).execute()

    @staticmethod
    def update_name_by_id(task_id: int, new_name: str) -> None:
        Task.update(name=new_name).where(Task.id == task_id).execute()

    @staticmethod
    def update_description_by_id(task_id: int, new_description: str) -> None:
        Task.update(description=new_description).where(Task.id == task_id).execute()

    @staticmethod
    def update_status_by_id(task_id: int, new_status: str) -> None:
        Task.update(status=new_status).where(Task.id == task_id).execute()

    def to_beauty_str(self) -> str:
        return "Task info:\nName - {name}\nDescription - {description}\nStatus - {status}".format(
            name=self.name,
            description=self.description,
            status=self.status
        )


database.create_tables([User, Meeting, Task])

logging.info("Database tables created successfully")
logging.info("Database is ready for using")
