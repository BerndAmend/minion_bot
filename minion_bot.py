#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
from telegram import KeyboardButton, ReplyKeyboardMarkup

import logging
import importlib
from os.path import expanduser

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

plugins = {}

class LimitToUser(BaseFilter):
    def __init__(self, authorized_users):
        self.authorized_users = authorized_users
    def filter(self, message):
        if message.from_user.id in self.authorized_users:
            return True
        else:
            logger.info("Ignored message from unauthorized user %s" % message)
            return False

def start(bot, update):
    logger.info('Start "%s" \n' % update.message)
    update.message.reply_text('Hi!')
    kb = [[KeyboardButton('activate'), KeyboardButton('deactivate')],
          [KeyboardButton('show me'), KeyboardButton('move it')]]
    kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)

    bot.send_message(chat_id=update.message.chat_id,
                     text="Welcome!",
                     reply_markup=kb_markup)

def handlemessage(bot, update):
    logger.info('Received "%s"\n' % update.message)

    for k, v in plugins.items():
        if v.handlemessage(bot, update.message):
            logger.info("Message handled by %s" % k)
            return

    if update.message.text.lower() == 'so what?':
        helpdict = {"so what?": "available commands"}

        for k, v in plugins.items():
            helpdict.update(v.helpmessage())

        helptext = ""
        for k, v in helpdict.items():
            helptext += "'" + k + "' - " + v + "\n"

        update.message.reply_text(helptext)
    else:
        update.message.reply_text("What ya sayin', dog?")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def main():
    home = expanduser("~")
    try:
        config = json.load(open('%s/.minion_bot.json' % home))
    except FileNotFoundError:
        print('move minion_bot.json to home directory ~/.minion_bot.json')
        sys.exit(-1)

    limit_to_user = LimitToUser(config['telegram']['users'])

    updater = Updater(token=config['telegram']['token'])
    dp = updater.dispatcher

    global plugins
    for k,v in config.items():
        if k == "telegram":
            {}
        elif v["enable"]:
            print('load plugin %s' % k)
            try:
                loadedplugin = importlib.__import__("plugins.%s" % k, fromlist=[k]).__export__
                plugins[k] = loadedplugin(v, dp)
            except:
                print("Couldn't load plugin %s" % k)

    print('Done')

    dp.add_handler(CommandHandler("start", start, limit_to_user))
    dp.add_handler(MessageHandler(Filters.text & limit_to_user, handlemessage))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
