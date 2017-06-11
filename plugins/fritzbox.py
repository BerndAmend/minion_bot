import urllib.request
import xml.etree.ElementTree as ET
import hashlib
from IPlugin import IPlugin

# add proper error handling
class FritzBox(IPlugin):

    def __init__(self, config):
        self.config = config
        self.address = config['address']
        self.authenticate(config['username'], config['password'])

    def handlemessage(self, bot, msg):
        cmd = msg.text.lower().split(' ')
        if len(cmd) != 2:
            return False

        if cmd[0] != "fritz":
            return False

        if cmd[1] == "create":
            self.createportforwardings()
        elif cmd[1] == "delete":
            for i in range(len(self.config['ports'])):
                self.request('data.lua',
                             f"lang=de&no_sidrenew=&delete_portrule=rule0&oldpage=%2Finternet%2Fport_fw.lua")
        elif cmd[1] == "enable":
            self.request('data.lua',
                         'lang=de&no_sidrenew=&active_9=1&active_8=1&active_7=1&active_6=1&active_5=1&active_4=1&active_3=1&active_2=1&active_1=1&apply=&oldpage=%2Finternet%2Fport_fw.lua')
        elif cmd[1] == "disable":
            self.request('data.lua',
                         'lang=de&no_sidrenew=&apply=&oldpage=%2Finternet%2Fport_fw.lua')

        msg.reply_text("Done")
        return True

    def createportforwardings(self):
        for f in self.config['ports']:
            rule = "rule%s" % f['rule']
            self.request('data.lua',
                         f"lang=de&no_sidrenew=&current_rule={rule}&current_exposed_rule=exposed_host0&is_new_rule=true&was_exposed_host=false&forwardrules_{rule}_activated=1&selected_app=other&forwardrules_{rule}_description={f['name']}&forwardrules_{rule}_protocol=TCP&forwardrules_{rule}_port={f['port']}&forwardrules_{rule}_endport={f['endport']}&selected_lan_device=manuell%23manuell&forwardrules_{rule}_fwip={f['ip']}&forwardrules_{rule}_fwport={f['fwport']}&rule={rule}&apply=&oldpage=%2Finternet%2Fport_fw_edit.lua")

    def authenticate(self, username, password):
        request = ET.fromstring(urllib.request.urlopen('http://' + self.address + '/login_sid.lua').read())
        self.sid = request[0].text
        if self.sid == '0000000000000000':
            challenge = request[1].text
            response = challenge + '-' + hashlib.md5(str(challenge + '-' + password).encode('utf-16le')).hexdigest()
            request = ET.fromstring(urllib.request.urlopen('http://' + self.address + '/login_sid.lua?username=' + username + '&response=' + response).read())
            self.sid = request[0].text

    def request(self, func, args):
        urllib.request.urlopen('http://' + self.address + '/' + func + '?xhr=1&sid=' + self.sid + '&' + args).read()

__export__ = FritzBox
