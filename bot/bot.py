""" 
This file includes all business logic of bot.
All handlers are only here.
"""
import datetime
import logging

import telebot

import bot.config as config
import bot.database as db
import bot.markups as markups

bot = telebot.TeleBot(config.bot_token, parse_mode=None)

current_year = datetime.datetime.now().year


@bot.message_handler(
    commands=['start'],
    func=lambda message: not db.User.is_user_exists(message.chat.id)
)
def start_handler(message):
    bot.send_message(message.chat.id, "Howdy! What's your name, dude?")
    bot.register_next_step_handler(message, callback=saving_name_handler)

    logging.info("New user with telegram id {} started bot".format(message.chat.id))


def saving_name_handler(message):
    bot.send_message(
        message.chat.id,
        "Okay, {name} is enough good name for me.\nNice to meet you, {name}!".format(name=message.text)
    )

    db.User.create(
        tg_id=message.chat.id,
        name=message.text
    )

    logging.info(
        "New user's name {name} has been saved to database, user's telegram id is {id}".format(
            name=message.text, id=message.chat.id
        )
    )


@bot.message_handler(
    commands=['new_task'],
    func=lambda message: db.User.is_user_exists(message.chat.id)
)
def new_task_handler(message):
    logging.info("User {tg_id} started creating new task".format(tg_id=message.chat.id))

    user = db.User.get_by_tg_id(message.chat.id)
    bot.send_message(
        message.chat.id,
        "{name}, enter name of the new task, please".format(name=user.name.capitalize())
    )

    bot.register_next_step_handler(
        message,
        callback=new_task_name_handler,
        user=user
    )


def new_task_name_handler(message, user: db.User):
    logging.info("User {tg_id} entered name for the new task".format(tg_id=message.chat.id))

    bot.send_message(
        message.chat.id,
        "{name}, enter description of the new task, please".format(name=user.name.capitalize())
    )

    bot.register_next_step_handler(
        message,
        callback=new_task_description_handler,
        user=user,
        name=message.text
    )


def new_task_description_handler(message, user: db.User, name: str):
    db.Task.create(
        name=name,
        description=message.text,
        user=user
    )

    bot.send_message(
        message.chat.id,
        "New task is ready, it has been added to your task list"
    )

    logging.info(
        "User {tg_id} entered description for the new task and finished creating task".format(tg_id=message.chat.id)
    )


# TODO: create scheduling
@bot.message_handler(
    commands=['new_meeting'],
    func=lambda message: db.User.is_user_exists(message.chat.id)
)
def new_meeting_handler(message):
    logging.info("User {tg_id} started creating new meeting".format(tg_id=message.chat.id))

    bot.send_message(
        message.chat.id,
        "Choose year",
        reply_markup=markups.gen_years_markup(
            [i for i in range(current_year, current_year + 5)]
        )
    )


def new_meeting_name_handler(message, user: db.User, due_date: datetime.datetime):
    logging.info("User {tg_id} entered name for the new meeting".format(tg_id=message.chat.id))

    bot.send_message(
        message.chat.id,
        "{name}, enter description of the new meeting, please".format(name=user.name.capitalize())
    )

    bot.register_next_step_handler(
        message,
        callback=new_meeting_description_handler,
        user=user,
        name=message.text,
        due_date=due_date
    )


def new_meeting_description_handler(message, user: db.User, name: str, due_date: datetime.datetime):
    db.Meeting.create(
        name=name,
        description=message.text,
        date=due_date,
        user=user
    )

    bot.send_message(
        message.chat.id,
        "New meeting is ready, it has been added to your meeting list"
    )

    logging.info("User {tg_id} finished creating of the new meeting".format(tg_id=message.chat.id))


@bot.callback_query_handler(
    func=lambda call:
    db.User.is_user_exists(call.message.chat.id)
    and
    call.data.split()[0] in [
        "year",
        "month",
        "day",
        "hour",
        "minute"
    ]
)
def callback_datetime_handler(call):
    data = call.data.split()

    text = None
    markup = None

    if data[0] == "year":
        text = "Choose month"
        markup = markups.gen_months_markup(
            int(data[1])
        )
    elif data[0] == "month":
        text = "Choose day"
        markup = markups.gen_days_markup(
            int(data[1]),
            int(data[2])
        )
    elif data[0] == "day":
        text = "Choose hour"
        markup = markups.gen_hours_markup(
            int(data[1]),
            int(data[2]),
            int(data[3])
        )
    elif data[0] == "hour":
        text = "Choose minute"
        markup = markups.gen_minutes_markup(
            int(data[1]),
            int(data[2]),
            int(data[3]),
            int(data[4])
        )
    elif data[0] == "minute":
        logging.info("User {tg_id} entered datetime of the new meeting".format(tg_id=call.message.chat.id))

        user = db.User.get_by_tg_id(call.message.chat.id)

        text = "{name}, enter name of the new meeting, please".format(name=user.name.capitalize())

        bot.register_next_step_handler(
            call.message,
            callback=new_meeting_name_handler,
            user=user,
            due_date=datetime.datetime(
                year=int(data[1]),
                month=int(data[2]),
                day=int(data[3]),
                hour=int(data[4]),
                minute=int(data[5])
            )
        )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=text,
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(
        message.chat.id,
        "It's list of available commands:\n" +
        "/new_task - Create new task\n" +
        "/new_meeting - Create new meeting\n" +
        "/task_edit - Edit task(not ready)\n" +
        "/meeting_edit - Edit meeting(not ready)\n" +
        "/task_list - List tasks\n" +
        "/meeting_list - List meetings\n" +
        "/delete_task - Delete task\n" +
        "/delete_meeting - Delete meeting(not ready)\n" +
        "/exit - Delete all my info\n" +
        "/help - Print this help message"
    )


@bot.message_handler(
    commands=['exit'],
    func=lambda message: db.User.is_user_exists(message.chat.id)
)
def exit_handler(message):
    logging.info("User {tg_id} wants to delete account".format(tg_id=message.chat.id))
    user = db.User.get_by_tg_id(message.chat.id)

    bot.send_message(
        message.chat.id,
        "Delete everything, {name}?".format(name=user.name),
        reply_markup=markups.gen_yes_no_markup()
    )

    bot.register_next_step_handler(
        message,
        callback=yes_no_exit_handler,
        user=user
    )


def yes_no_exit_handler(message, user: db.User):
    if message.text == "Yes":
        bot.send_message(
            message.chat.id,
            "Okay, i was glad to meet you. Good luck, {name}".format(name=user.name),
            reply_markup=markups.gen_delete_markup()
        )

        db.User.delete_cascade(message.chat.id)

        logging.info("User {tg_id} has been deleted his account".format(tg_id=message.chat.id))
    else:
        bot.send_message(
            message.chat.id,
            "Nevermind, i'll forget about this accident",
            reply_markup=markups.gen_delete_markup()
        )

        logging.info(
            "User {tg_id} has changed his opinion and hasn't deleted his account".format(tg_id=message.chat.id))


@bot.message_handler(
    commands=['task_list'],
    func=lambda message: db.User.is_user_exists(message.chat.id)
)
def task_list_handler(message):
    logging.info("User {tg_id} requested task list".format(tg_id=message.chat.id))

    user = db.User.get_by_tg_id(message.chat.id)
    tasks = db.Task.get_by_user(user)

    if len(tasks) > 0:

        bot.send_message(
            message.chat.id,
            "Here:"
        )

        for task in tasks:
            bot.send_message(
                message.chat.id,
                "Name:\n{name}\nDescription:\n{description}\nStatus:\n{status}".format(
                    name=task.name,
                    description=task.description,
                    status=task.status
                )
            )
    else:
        bot.send_message(
            message.chat.id,
            "It's empty, but you can use /new_task for creating"
        )


@bot.message_handler(
    commands=['meeting_list'],
    func=lambda message: db.User.is_user_exists(message.chat.id)
)
def meeting_list_handler(message):
    logging.info("User {tg_id} requested meeting list".format(tg_id=message.chat.id))

    user = db.User.get_by_tg_id(message.chat.id)
    meetings = db.Meeting.get_by_user(user)

    if len(meetings) > 0:

        bot.send_message(
            message.chat.id,
            "Here:"
        )

        for meeting in meetings:
            bot.send_message(
                message.chat.id,
                "Name:\n{name}\nDescription:\n{description}\nDate:\n{date}".format(
                    name=meeting.name,
                    description=meeting.description,
                    date=meeting.date
                )
            )
    else:
        bot.send_message(
            message.chat.id,
            "It's empty, but you can use /new_meeting for creating"
        )


@bot.message_handler(
    commands=['delete_task'],
    func=lambda message: db.User.is_user_exists(message.chat.id)
)
def delete_task_handler(message):
    logging.info("User {tg_id} wants to delete task".format(tg_id=message.chat.id))

    user = db.User.get_by_tg_id(message.chat.id)
    tasks = db.Task.get_by_user(user)

    bot.send_message(message.chat.id, "Tasks:")

    for task in tasks:
        bot.send_message(
            message.chat.id,
            "{name} - {status}".format(name=task.name.capitalize(), status=task.status),
            reply_markup=markups.gen_delete_task_markup(task.id)
        )


@bot.callback_query_handler(
    func=lambda call:
    db.User.is_user_exists(call.message.chat.id)
    and
    call.data.split()[0] == "delete"
)
def callback_delete_task_handler(call):
    task_id = int(call.data.split()[1])

    logging.info("User {tg_id} deleting task {task_id}".format(
        tg_id=call.message.chat.id,
        task_id=task_id
    ))

    db.Task.delete_by_id(task_id)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text="Deleted"
    )


@bot.message_handler()
def wrong_command_handler(message):
    bot.reply_to(message, "Sorry, but i don't understand you, dude")
    logging.info("Wrong command has been denied")


if __name__ == '__main__':
    logging.info("Bot launched directly")
    bot.polling(none_stop=True)
