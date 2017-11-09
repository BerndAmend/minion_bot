from IPlugin import IPlugin
import subprocess

# add proper error handling
class Updater(IPlugin):

    def __init__(self, config, dispatcher):
        return

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'update yourself!':
            output = subprocess.check_output("git pull --ff-only", shell=True)
            msg.reply_text(output.decode("utf-8"))
            return True
        else:
            return False
    
    def helpmessage(self):
        return {"update yourself!": "get the newest version of minion_bot"}

__export__ = Updater
