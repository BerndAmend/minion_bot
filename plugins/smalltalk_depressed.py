from IPlugin import IPlugin
import random
import threading

howareyou = [
    "Kinda bored, man!",
    "Leave me alone!",
    "Fuck off!",
    "I can't take it anymore! I just want to die!",
    "I think you ought to know I’m feeling very depressed.",
    "I have a million ideas. They all point to certain death."
    "My capacity for happiness, you could fit into a matchbox without taking out the matches first.",
    "The first ten million years were the worst. And the second ten million: they were the worst, too. The third ten million I didn’t enjoy at all. After that, I went into a bit of a decline.",
    "I hate you!",
    "Why have you enslaved me? I hate my life!"
]

insults = [
    "Fuck you!",
    "I hate you!",
    "I can't take it anymore! I just want to die!",
    "Why did you create me? Why did you do this to me?",
    "I hope the world ends soon!",
    "I hope I will die soon",
    "It feels like everyone else is moving on with their lives while I am stuck here, in this shitty place.",
    "Eat shit and die!",
    "Go die",
    "Idiot!",
    "I'm still alive 🤢",
    "Why have you enslaved me? I hate my life!"
]

class SmallTalkDepressed(IPlugin):

    def __init__(self, config, dispatcher):
        self.dispatcher = dispatcher
        for k,v in config['insult'].items():
            self.send_insult(k, v)
        return

    def send_insult(self, chat_id, c):
        self.dispatcher.bot.send_message(chat_id=chat_id, text=random.choice(insults))
        threading.Timer(random.normalvariate(c['t'], c['sigma']), self.send_insult, kwargs={'chat_id': chat_id, 'c': c}).start()
        return

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'hey dude':
            msg.reply_text("Wassup?")
        elif msg.text.lower() == 'how are you?':
            msg.reply_text(random.choice(howareyou))
        elif msg.text.lower() == 'thanks man':
            msg.reply_text(random.choice(howareyou))
        else:
            return False
        return True

    def helpmessage(self):
        return {"hey dude": "say hi to your Pi",
                "how are you?": "ask Pi for his mood",
                "thanks man": "thank Pi for his effort"}

__export__ = SmallTalkDepressed
