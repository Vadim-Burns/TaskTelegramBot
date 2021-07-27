""" 
This file includes all business logic of bot.
All handlers are only here.
"""

import logging

import telebot

import bot.config as config
import bot.database as db

bot = telebot.TeleBot(config.bot_token, parse_mode=None)


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
        user=user,
        name=name,
        description=message.text
    )

    bot.send_message(
        message.chat.id,
        "New task is ready, it has been added to your task list"
    )

    logging.info(
        "User {tg_id} entered description for the new task and finished creating task".format(tg_id=message.chat.id)
    )


@bot.message_handler()
def wrong_command_handler(message):
    bot.reply_to(message, "Sorry, but i don't understand you, dude")
    logging.info("Wrong command has been denied")


if __name__ == '__main__':
    logging.info("Bot launched directly")
    bot.polling(none_stop=True)
