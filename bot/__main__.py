"""
This file manages the initialization process of bot.
"""

import logging

from bot import bot

# TODO: add flask server for webhooks
logging.info("Starting service initialization process")

bot.bot.polling(none_stop=True)

logging.info("Bot finished")
