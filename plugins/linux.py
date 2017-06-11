from datetime import timedelta
from IPlugin import IPlugin
import os

# add proper error handling
class Linux(IPlugin):

    def __init__(self, config):
        return

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'awake?':
            td = self.uptime()
            days = td.days
            hours, remainder = divmod(td.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            msg.reply_text("Yeah man, for " + str(days) + " days, " + str(hours) + " hours, and " + str(minutes) + " minutes now!")
            return True
        elif msg.text.lower() == 'reboot dude':
            msg.reply_text("Gonna reboot now, pal!")
            os.system("sudo shutdown -r now")
            return True
        elif msg.text.lower() == 'go to sleep':
            msg.reply_text("Alright, good night, man!")
            os.system("sudo shutdown now")
            return True
        else:
            return False

    def uptime(self):
        with open('/proc/uptime', 'r') as f:
            return timedelta(seconds=float(f.readline().split()[0]))

__export__ = Linux
