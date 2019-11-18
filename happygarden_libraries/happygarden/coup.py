import os, subprocess, json, time, pexpect

class RemoteCoup():
    SETUP_CMD = """from happygarden.mycoup import *; c = Coup()"""
    STATUS_CMD = """c.get_status()"""
    SET_STATE_CMD = """c.set_light_mode({0})"""
    PROMPT = '>>> '

    status = None
    user = None
    device = None
    session = None

    def __init__(self, user, pi_device, **kwargs):
        self.user = user
        self.device = pi_device
        self.session = pexpect.spawn("ssh {0}@{1} -t python3".format(self.user, self.device))
        self.session.expect(self.PROMPT)
        self.session.sendline(self.SETUP_CMD)
        self.session.expect(self.PROMPT)
        self.refresh_status()

    def refresh_status(self):
        self.session.sendline(self.STATUS_CMD)
        self.session.expect("""{.*}""")
        self.status = json.loads(self.session.after)
        self.session.expect(self.PROMPT)

    def set_light_mode(self, mode):
        print('setting mode: ' + self.SET_STATE_CMD.format(mode))
        self.session.sendline(self.SET_STATE_CMD.format(mode))
        self.session.expect(self.PROMPT)
        self.refresh_status()
       
my_coup = RemoteCoup('pi','10.0.10.200')
print('coup status: {}'.format(my_coup.status))
my_coup.set_light_mode('LIGHT_MODE.PRE_BED.value')
print('coup status: {}'.format(my_coup.status))
my_coup.set_light_mode('LIGHT_MODE.ALL_OFF.value')
print('coup status: {}'.format(my_coup.status))
my_coup.set_light_mode('LIGHT_MODE.ALL_ON.value')
print('coup status: {}'.format(my_coup.status))

# my_coup.session.interact()