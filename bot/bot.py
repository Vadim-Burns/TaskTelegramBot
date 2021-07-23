"""
This file includes all business logic of bot.
All handlers are only here.
"""

import telebot
import config
import database as db

bot = telebot.TeleBot(config.bot_token, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Howdy! What's your name, dude?")
    bot.register_next_step_handler(message, callback=saving_name_handler)


def saving_name_handler(message):
    bot.send_message(
        message.chat.id,
        "Okay, {name} is enough good name for me.\nNice to meet you, {name}!".format(name=message.text)
    )


@bot.message_handler(content_types=['text'])
def wrong_command_handler(message):
    bot.reply_to(message, "Sorry, but i don't understand you, dude")


if __name__ == '__main__':
    bot.polling(none_stop=True)
