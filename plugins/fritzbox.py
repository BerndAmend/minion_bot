import urllib.request
import xml.etree.ElementTree as ET
import hashlib
from IPlugin import IPlugin

# add proper error handling
class FritzBox(IPlugin):

    def __init__(self, config):
        self.authenticate(config['username'], config['password'])

    def handlemessage(self, bot, msg):
        return False

    def authenticate(self, username, password):
        request = ET.fromstring(urllib.request.urlopen("http://fritz.box/login_sid.lua").read())
        self.sid = request[0].text
        if self.sid == '0000000000000000':
            challenge = request[1].text
            response = challenge + '-' + hashlib.md5(str(challenge + '-' + password).encode('utf-16le')).hexdigest()
            request = ET.fromstring(urllib.request.urlopen('http://fritz.box/login_sid.lua?username=' + username + '&response=' + response).read())
            self.sid = request[0].text

    def request(self, func, args):
        urllib.request.urlopen('http://fritz.box/' + func + '?xhr=1&sid=' + self.sid + '&' + args).read()

__export__ = FritzBox