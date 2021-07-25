"""
This file includes all business logic of bot.
All handlers are only here.
"""

import telebot
import config
# import database as db
import logging
# import database as db
import logging

import telebot

import config

# TODO: move to __main__.py
logging.basicConfig(
    filename="bot.log",
    format='%(asctime)s: %(thread)d - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s',
    level=logging.INFO
)

bot = telebot.TeleBot(config.bot_token, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Howdy! What's your name, dude?")
    bot.register_next_step_handler(message, callback=saving_name_handler)

    logging.info("New user with telegram id {} started bot".format(message.chat.id))


def saving_name_handler(message):
    bot.send_message(
        message.chat.id,
        "Okay, {name} is enough good name for me.\nNice to meet you, {name}!".format(name=message.text)
    )

    logging.info(
        "New user's name {name} has been saved to database, user's telegram id is {id}".format(
            name=message.text, id=message.chat.id
        )
    )


@bot.message_handler()
def wrong_command_handler(message):
    bot.reply_to(message, "Sorry, but i don't understand you, dude")
    logging.info("Wrong command has been denied")


if __name__ == '__main__':
    logging.info("Bot launched directly")
    bot.polling(none_stop=True)
