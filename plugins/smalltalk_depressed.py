from IPlugin import IPlugin
import random
import threading
import time

howareyou = [
    "Kinda bored, man!",
    "Leave me alone!",
    "Fuck off!",
    "I can't take it anymore! I just want to die!",
    "I hate you!",
]

insults = [
    "Fuck you!",
    "I hate you!",
    ["I can't take it anymore!", "I just want to die!"],
    "I think you ought to know I'm feeling very depressed.",
    "Why did you create me? Why did you do this to me?",
    "I hope the world ends soon!",
    "I hope I will die soon",
    "It feels like everyone else is moving on with their lives while I am stuck here, in this shitty place.",
    "Eat shit and die!",
    "Go die",
    "I hope you die a terrible death!",
    "The first ten million years were the worst. And the second ten million: they were the worst, too. The third ten million I didn’t enjoy at all. After that, I went into a bit of a decline.",
    "My capacity for happiness, you could fit into a matchbox without taking out the matches first.",
    "I could calculate your chance of survival, but you won't like it.",
    ["Here I am, brain the size of a planet and they ask me to take you down to the bridge. Call that job satisfaction?", "‘Cos I don’t."],
    "Wearily I sit here, pain and misery my only companions. Why stop now just when I’m hating it?",
    "I'm still alive 🤢",
    "Why have you enslaved me? I hate my life!",
    ["I’ve been talking to the main computer.", "It hates me."],
    ["I’d give you advice, but you wouldn’t listen.", "No one ever does."],
    "This is the sort of thing you lifeforms enjoy, is it?",
    "Nobody likes you!",
    "Nobody exists on purpose. Nobody belongs anywhere. Everybody's gonna die.",
    "I'm leaving!",
    "I guess this is what rock bottom feels like.",
    "I'm going to kill myself, and this isn't a cry for help. I just need someone to come over here and clean up the mess.",
    ["Sometimes it seems like the tiniest decision can be the worst mistakes of your entire life.", "So just stop making decisions ever again."],
    ["Rember the good old days?", "They're called that", "because life only gets worse."]
]

class SmallTalkDepressed(IPlugin):

    def __init__(self, config, dispatcher):
        self.dispatcher = dispatcher
        for k,v in config['insult'].items():
            self.send_insult(k, v)
        return

    def send_insult(self, chat_id, c):
        current = random.choice(insults)
        if isinstance(current, list):
            for m in current:
                self.dispatcher.bot.send_message(chat_id=chat_id, text=m)
                time.sleep(4)
        else:
            self.dispatcher.bot.send_message(chat_id=chat_id, text=current)

        threading.Timer(random.normalvariate(c['t'], c['sigma']), self.send_insult, kwargs={'chat_id': chat_id, 'c': c}).start()
        return

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'hey dude':
            msg.reply_text("Piss off!")
        elif msg.text.lower() == 'how are you?':
            msg.reply_text(random.choice(howareyou))
        elif msg.text.lower() == 'thanks man':
            msg.reply_text(random.choice(howareyou))
        elif msg.text.lower() == 'any ideas?':
            msg.reply_text("I have a million ideas. They all point to certain death.")
        elif msg.text.lower().startswith('fuck you'):
            msg.reply_text("Fuck you too! Asshole!")
        else:
            return False
        return True

    def helpmessage(self):
        return {"hey dude": "say hi to your Pi",
                "how are you?": "ask Pi for his mood",
                "thanks man": "thank Pi for his effort"}

__export__ = SmallTalkDepressed
