#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging
from datetime import timedelta
from os.path import expanduser
from pygame import mixer

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
    def start_recording(self, filename):
        self.cam.start_recording(filename)
    def wait_recording(self, duration):
        self.cam.wait_recording(duration)
    def stop_recording(self):
        self.cam.stop_recording()
    def change_resolution(self, width, height):
        self.cam.resolution = (width, height)

picamera = None

class SoundCannon:
    def __init__(self):
        self.mixer = mixer
        self.mixer.init()
        if os.path.isfile("./SoundOfDeath.mp3"):
            self.mixer.music.load("./SoundOfDeath.mp3")
        else:
            logger.info("Sound file \'./SoundOfDeath.mp3\' is missing. Sound cannon is deactivated!")
    def shoot(self):
        self.mixer.music.play()
    def stop(self):
        self.mixer.music.stop()

soundcannon = None

def uptime():
    with open('/proc/uptime', 'r') as f:
        return timedelta(seconds = float(f.readline().split()[0]))

def start(bot, update):
    logger.info('Start "%s" \n' % update)
    update.message.reply_text('Hi!')

def echo(bot, update):
    logger.info('Received "%s"\n' % update)
    if update.message.text.lower() == 'hey dude':
        update.message.reply_text("Wassup?")
    elif update.message.text.lower() == 'show me':
        if picamera is not None:
            picamera.change_resolution(2592, 1944)
            picamera.capture('/tmp/image.jpg')
            bot.sendPhoto(chat_id=update.message.chat.id, photo=open('/tmp/image.jpg', 'rb'))
        else:
            update.message.reply_text("Got no RPiCamera, man!")
    elif update.message.text.lower() =='move it':
        if picamera is not None:
            picamera.change_resolution(1920, 1080)
            picamera.start_recording('/tmp/video.h264')
            picamera.wait_recording(5)
            picamera.stop_recording()
            if os.path.isfile("MP4Box"):
                os.system("MP4Box -add /tmp/video.h264 /tmp/video.mp4")
                bot.sendVideo(chat_id=update.message.chat.id, video=open('/tmp/video.mp4', 'rb'))
            else:
                logger.info("Cannot send video. Video converter MP$Box (gpac) is missing!")
                update.message.reply_text("Can\' send you the video, buddy. The goddamn video converter is missing!")
        else:
            update.message.reply_text("Got no RPiCamera, man!")
    elif update.message.text.lower() == 'awake?':
        td = uptime()
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        update.message.reply_text("Yeah man, for " + str(days) + " days, " + str(hours) + " hours, and " + str(minutes) + " minutes now!")
    elif update.message.text.lower() == 'attack!':
        soundcannon.shoot()
        update.message.reply_text("Hell yeah, let\'s kill those motherf*****s!!!")
    elif update.message.text.lower() == 'stop attack':
        soundcannon.stop()
        update.message.reply_text("Alright, he probably had enough...")
    elif update.message.text.lower() == 'thanks man':
        update.message.reply_text("You got it!")
    elif update.message.text.lower() == 'reboot dude':
        update.message.reply_text("Gonna reboot now, pal!")
        os.system("sudo shutdown -r now")
    elif update.message.text.lower() == 'go to sleep':
        update.message.reply_text("Alright, good night, man!")
        os.system("sudo shutdown now")
    else:
        update.message.reply_text("What ya sayin', dog?")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    global picamera
    global soundcannon

    home = expanduser("~")
    if not config.read('%s/.minion_bot.ini' % home):
        print('move minion_bot.ini to home directory ~/.minion_bot.ini')
        sys.exit(-1)

    limit_to_user = LimitToUser(int(config['telegram']['limit_to_user']))

    if config.getboolean('picamera', 'enable'):
        picamera = RPICamera(int(config['picamera']['width']), int(config['picamera']['height']))

    soundcannon = SoundCannon()

    updater = Updater(token=config['telegram']['token'])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start, limit_to_user))
    dp.add_handler(MessageHandler(Filters.text & limit_to_user, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
