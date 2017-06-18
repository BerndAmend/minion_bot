from picamera import PiCamera
from IPlugin import IPlugin
from threading import Thread
import os

class RPICamera(IPlugin):
    def __init__(self, config):
        width = int(config['width'])
        height = int(config['height'])
        framerate = int(config['framerate'])
        self.cam = PiCamera()
        self.cam.resolution = (width, height)
        self.cam.framerate = framerate
        self.cam.start_preview()

    def start_motiondet(self):
        t = Thread(target=self.update)
        t.daemon = True
        t.start()
        return self

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

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'show me':
            self.change_resolution(2592, 1944)
            self.capture('/tmp/image.jpg')
            bot.sendPhoto(chat_id=msg.chat.id, photo=open('/tmp/image.jpg', 'rb'))
            return True
        elif msg.text.lower() == 'move it':
            os.system("rm /tmp/video.h264")
            self.change_resolution(1920, 1080)
            self.start_recording('/tmp/video.h264')
            self.wait_recording(5)
            self.stop_recording()
            if os.path.isfile("/usr/bin/MP4Box"):
                os.system("MP4Box -new -fps " + str(self.cam.framerate) + " -add /tmp/video.h264 /tmp/video.mp4")
                bot.sendVideo(chat_id=msg.chat.id, video=open('/tmp/video.mp4', 'rb'))
            else:
                #logger.info("Cannot send video. Video converter MP4Box (gpac) is missing!")
                msg.reply_text("Can\'t send you the video, buddy. The goddamn video converter is missing!")
            return True
        return False

__export__ = RPICamera
