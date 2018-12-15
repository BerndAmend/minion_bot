from IPlugin import IPlugin
import os
import time
import sys
import cv2

class CVCamera(IPlugin):
    def __init__(self, config, dispatcher):
        True

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'show me 2':
            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            ret, frame = cam.read()
            if ret == True:
                cv2.imwrite('/tmp/image.jpg', frame)
                bot.sendPhoto(chat_id=msg.chat.id, photo=open('/tmp/image.jpg', 'rb'))
            else:
                msg.reply_text("Couldn't read image")
            return True
        return False
      
    def helpmessage(self):
        return {"show me 2": "get single image"}

__export__ = CVCamera
