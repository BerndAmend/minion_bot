#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging
from datetime import timedelta
from os.path import expanduser

class NotInstalled(object):
    def __init__(self, name):
        self.__name = name

    def __getattr__(item):
        raise ImportError('The {0} package is required to use this '
                          'optional feature'.format(self.__name))

try:
    from picamera import PiCamera
except ImportError:
    PiCamera = NotInstalled(name='picamera')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()

class LimitToUser(BaseFilter):
    def __init__(self, limit_to_user):
        self.limit_to_user = limit_to_user
    def filter(self, message):
        return message.from_user.id == self.limit_to_user

class RPICamera:
    def __init__(self, width, height):
        self.cam = PiCamera()
        self.cam.resolution = (width, height)
        self.cam.start_preview()
    def capture(self, filename):
        self.cam.capture(filename)

picamera = None

def uptime():
    with open('/proc/uptime', 'r') as f:
        return str(timedelta(seconds = float(f.readline().split()[0])))

def start(bot, update):
    logger.info('Start "%s" \n' % update)
    update.message.reply_text('Hi!')

def echo(bot, update):
    logger.info('Received "%s"\n' % update)
    if update.message.text.lower() == 'show':
        if picamera is not None:
            picamera.capture('/tmp/image.jpg')
            bot.sendPhoto(chat_id=update.message.chat.id, photo=open('/tmp/image.jpg', 'rb'))
        else:
            update.message.reply_text("RPiCamera is disabled")
    elif update.message.text.lower() == 'up':
        update.message.reply_text(uptime())
    else:
        update.message.reply_text("I don't understand")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    global picamera

    home = expanduser("~")
    if not config.read('%s/.minion_bot.ini' % home):
        print('move minion_bot.ini to home directory ~/.minion_bot.ini')
        sys.exit(-1)

    limit_to_user = LimitToUser(int(config['telegram']['limit_to_user']))

    if config.getboolean('picamera', 'enable'):
        picamera = RPICamera(int(config['picamera']['width']), int(config['picamera']['height']))

    updater = Updater(token=config['telegram']['token'])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start, limit_to_user))
    dp.add_handler(MessageHandler(Filters.text & limit_to_user, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
