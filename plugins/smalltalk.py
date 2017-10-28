from IPlugin import IPlugin
import random

class SmallTalk(IPlugin):

    def __init__(self, config):
        return

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'hey dude':
            msg.reply_text("Wassup?")
        elif msg.text.lower() == 'how are you?':
            r = random.random();
            if r <= 0.7:
                msg.reply_text("Kinda bored, man!")
            elif r <= 0.8:
                msg.reply_text("Leave me alone!")
            elif r <= 0.9:
                msg.reply_text("Fuck off!")
            else:
                msg.reply_text("I can't take it anymore! I just want to die!")
        elif msg.text.lower() == 'thanks man':
            msg.reply_text("You got it!")
        else:
            return False
        return True

    def helpmessage(self):
        return {"hey dude": "say hi to your Pi",
                "how are you?": "ask Pi for his mood",
                "thanks man": "thank Pi for his effort"}

__export__ = SmallTalk
