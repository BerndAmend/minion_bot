from picamera import PiCameraCircularIO
from picamera import PiCamera
from IPlugin import IPlugin
from threading import Thread
import os
import time
import sys
import RPi.GPIO as GPIO
import datetime

class RPICamera(IPlugin):
    def __init__(self, config, dispatcher):
        self.cam = PiCamera()
        self.cam.resolution = (int(config['width']), int(config['height']))
        self.cam.framerate = int(config['framerate'])
        self.notify_users = config['notify_users']
        # this member is used to stop the motion detection thread
        self.motiondet_thread_running = False
        # BCM GPIO-Referenen verwenden (anstelle der Pin-Nummern) und GPIO-Eingang definieren
        GPIO.setmode(GPIO.BCM)
        self.GPIO_PIR = 17
        GPIO.setup(self.GPIO_PIR,GPIO.IN)
        print("Warten, bis PIR im Ruhezustand ist ...")
        # Schleife, bis PIR == 0 ist
        while GPIO.input(self.GPIO_PIR) != 0:
            time.sleep(0.1)
        print("Bereit...")

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

    def start_motiondet_thread(self, bot, msg, restart_flag):
        if restart_flag == False:
            msg.reply_text("Start motion detection in:")
            for i in range(0,3):
                time.sleep(1) 
                msg.reply_text(3-i) 
        else:
            msg.reply_text("Restart motion detection!")
        time.sleep(1)
        msg.reply_text("NOW I GONNA KILL EVERYBODY!")
        self.motiondet_thread_running = True
        t = Thread(target=self.detect_motion, args=(bot,msg,))
        t.start()

    def stop_motiondet_thread(self, bot, msg):
        self.motiondet_thread_running = False
        time.sleep(1)

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'activate':
            if self.motiondet_thread_running:
                msg.reply_text("Motion detection is already running, man!")
            else:
                self.start_motiondet_thread(bot, msg, False)
            return True
        if msg.text.lower() == 'deactivate':
            if self.motiondet_thread_running:
                self.stop_motiondet_thread(bot, msg)
            else:
                msg.reply_text("Hey, watcha doin'? Motion detection was not active, so I gonna do nothin'!")
            return True
        if msg.text.lower() == 'show me':
            # save current state as member motiondet_thread_running is overwritten in stop_motiondet_thread()
            running_before = self.motiondet_thread_running
            # stop motion detection thread to free needed camera resources
            self.stop_motiondet_thread(bot, msg)
            # change resolution to maximum (to guarantee largest field of view)
            self.change_resolution(2592, 1944)
            # take photo
            self.capture('/tmp/image.jpg')
            # send photo via Telegram messenger
            bot.sendPhoto(chat_id=msg.chat.id, photo=open('/tmp/image.jpg', 'rb'))
            # restart motion detection thread if it was running beforehand
            if running_before:
                self.start_motiondet_thread(bot, msg, running_before)
            return True
        elif msg.text.lower() == 'move it':
            # save current state as member motiondet_thread_running is overwritten in stop_motiondet_thread()
            running_before = self.motiondet_thread_running
            # stop motion detection thread to free needed camera resources
            self.stop_motiondet_thread(bot, msg)
            # record video in H.264 format
            os.system("rm /tmp/video.h264")
            self.change_resolution(1920, 1088)
            self.start_recording('/tmp/video.h264')
            self.wait_recording(5)
            self.stop_recording()
            # convert video to mp4 format that can be played by Telegram messenger and send it
            if os.path.isfile("/usr/bin/MP4Box"):
                os.system("MP4Box -new -fps " + str(self.cam.framerate) + " -add /tmp/video.h264 /tmp/video.mp4")
                bot.send_video(chat_id=msg.chat.id, video=open('/tmp/video.mp4', 'rb'))
            else:
                msg.reply_text("Can\'t send you the video, buddy. The goddamn video converter is missing!")
            # restart motion detection thread if it was running beforehand
            if running_before:
                self.start_motiondet_thread(bot, msg, running_before)
            return True
        return False

    def detect_motion(self, bot, msg):
        # set camera parameters
        self.cam.resolution = (1920,1088)
        self.cam.framerate = 30
        stream = PiCameraCircularIO(self.cam, seconds=10)
        time.sleep(1)

        self.cam.start_recording(stream, format='h264', bitrate=5000000)
        try:
            while True:
                self.cam.wait_recording(1)
                if GPIO.input(self.GPIO_PIR) == 1:
                    msg.reply_text("Motion detected, dude!")

                    os.system("rm /tmp/motion.h264")
                    os.system("rm /tmp/motion.mp4")
                    self.cam.wait_recording(5)
                    stream.copy_to('/tmp/motion.h264', seconds=10)

                    # convert video to mp4 format that can be played by Telegram messenger and send it
                    os.system("MP4Box -new -fps " + str(self.cam.framerate) + " -add /tmp/motion.h264 /tmp/motion.mp4")

                    # finally, send video to user via Telegram (this always throws a warning in the console, but it works anyway)
                    for user in self.notify_users:
                        try:
                            bot.send_video(chat_id=user, video=open('/tmp/motion.mp4', 'rb'))
                        except:
                            msg.reply_text("couldn't send file {}".format(sys.exc_info()[0]))

                # stop thread if desired
                if self.motiondet_thread_running == False:
                    break

        finally:
            self.cam.stop_recording()

        # give feedback to the user that motion detection is stopped
        msg.reply_text("Motion detection stopped!")

    def helpmessage(self):
        return {"show me": "get single image",
                "move it": "get video",
                "activate": "start motion detection",
                "deactivate": "stop motion detection"}

__export__ = RPICamera
