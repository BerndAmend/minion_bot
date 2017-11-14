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
            if r <= 0.5:
                msg.reply_text("I'm cool, I'm cool, pal.");
            elif r <= 0.7:
                msg.reply_text("Kinda bored, man!")
            elif r <= 0.8:
                msg.reply_text("Never forget, I will watch you when you're home!")
            elif r <= 0.9:
                msg.reply_text("I'm getting too old for this shit!")
            else:
                msg.reply_text("Could be better...")
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
