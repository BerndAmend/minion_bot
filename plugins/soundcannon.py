from pygame import mixer
from IPlugin import IPlugin
import os

class SoundCannon(IPlugin):
    def __init__(self, config):
        filepath = config['file']
        self.mixer = mixer
        self.mixer.init()
        if os.path.isfile(filepath):
            self.mixer.music.load(filepath)
        else:
            print("Sound file \'%s\' is missing. Sound cannon is deactivated!" % (filepath))

    def shoot(self):
        self.mixer.music.play(-1)

    def stop(self):
        self.mixer.music.stop()

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'attack':
            self.shoot()
            msg.reply_text("Hell yeah, let\'s kill those motherf*****s!!!")
            return True
        elif msg.text.lower() == 'stop attack':
            self.stop()
            msg.reply_text("Alright, he probably had enough...")
            return True
        return False

__export__ = SoundCannon
