from pygame import mixer
from IPlugin import IPlugin
import os

class SoundCannon(IPlugin):
    def __init__(self, config):
        self.mixer = mixer
        self.mixer.init()
        if os.path.isfile(config['file']):
            self.mixer.music.load(config['file'])
        else:
            print("Sound file \'./SoundOfDeath.mp3\' is missing. Sound cannon is deactivated!")

    def shoot(self):
        self.mixer.music.play()

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
