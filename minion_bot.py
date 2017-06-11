#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging
import importlib

from os.path import expanduser

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

plugins = {}

class LimitToUser(BaseFilter):
    def __init__(self, limit_to_users):
        self.limit_to_users = [int(x) for x in limit_to_users.split(',')]
    def filter(self, message):
        return message.from_user.id in self.limit_to_users

def start(bot, update):
    logger.info('Start "%s" \n' % update)
    update.message.reply_text('Hi!')

def handlemessage(bot, update):
    logger.info('Received "%s"\n' % update)

    for k, v in plugins.items():
        if v.handlemessage(bot, update.message):
            print("Message handled by %s" % k)
            return

    if update.message.text.lower() == 'hey dude':
        update.message.reply_text("Wassup?")
    elif update.message.text.lower() == 'thanks man':
        update.message.reply_text("You got it!")
    else:
        update.message.reply_text("What ya sayin', dog?")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def main():
    home = expanduser("~")
    config = configparser.ConfigParser()
    if not config.read('%s/.minion_bot.ini' % home):
        print('move minion_bot.ini to home directory ~/.minion_bot.ini')
        sys.exit(-1)

    limit_to_user = LimitToUser(config['telegram']['limit_to_users'])

    updater = Updater(token=config['telegram']['token'])
    dp = updater.dispatcher

    global plugins
    for plugin in config['plugins']:
        if config.getboolean('plugins', plugin):
            print('load plugin %s' % plugin)
            try:
                loadedplugin = importlib.__import__("plugins.%s" % plugin, fromlist=[plugin]).__export__
                c = {}
                try:
                    c = config[plugin]
                except KeyError:
                    pass
                plugins[plugin] = loadedplugin(c)
            except (AttributeError, NameError):
                print("Couldn't load plugin %s" % plugin)

    dp.add_handler(CommandHandler("start", start, limit_to_user))
    dp.add_handler(MessageHandler(Filters.text & limit_to_user, handlemessage))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
