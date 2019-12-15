import sys, json, time, pexpect, logging

logger = logging.getLogger(__name__)

class RemoteCoup():

    SETUP_CMD = """from happygarden.mycoup import *; c = Coup()"""
    STATUS_CMD = """c.get_status()"""
    SET_LIGHT_MODE_CMD = """c.set_light_mode({0})"""
    SET_STATE_CMD = """c.set_state('{0}')"""
    PROMPT = '>>> '
    STATUS_TIMEOUT = 10

    _connected = False
    _status = None
    _status_refreshed = None

    def __init__(self, user, pi_device, change_listener=None, **kwargs):
        self.user = user
        self.device = pi_device
        if self._check_session():
            self._refresh_status()

    def _check_response(self, expected):
        response = self._session.expect([pexpect.TIMEOUT, expected])
        if response == 0:
            _connected = False
            raise TimeoutError(self._session.before + self._session.after)

    def _spawn_session(self):
        try:
            self._session = pexpect.spawn("ssh {0}@{1} -t python3".format(self.user, self.device), timeout=5)
            self._check_response(self.PROMPT)
            self._session.sendline(self.SETUP_CMD)
            self._check_response(self.PROMPT)
            self._connected = True
        except:
            logger.error("Coup is not accessible: {0}".format(sys.exc_info()))
            self._connected = False
        
        return self._connected

    def _check_session(self):
        if (not self._connected) or (self._session is None) or (not self._session.isalive):
            return self._spawn_session()
        return True

    def _refresh_status(self):
        if self._check_session():
            self._session.sendline(self.STATUS_CMD)
            self._check_response("""{.*}""")
            logger.error(self._session.after)
            self._status = json.loads(self._session.after)
            self._check_response(self.PROMPT)
            self._status_refreshed = time.time()
    
    def get_status(self):
        if self._check_session():
            if (self._status is None) or (time.time() - self._status_refreshed > self.STATUS_TIMEOUT):
                self._refresh_status()
        else:
            self._status = None
        
        return self._status

    def set_light_mode(self, mode):
        if self._check_session():
            self._session.sendline(self.SET_LIGHT_MODE_CMD.format(mode))
            self._check_response(self.PROMPT)
            self._refresh_status()
    
    def apply_status(self, status):
        if self._check_session():
            self._session.sendline(self.SET_STATE_CMD.format(json.dumps(status)))
            self._check_response(self.PROMPT)
            logger.debug("Command-line return text: %s", self._session.before)
            self._refresh_status()
       
# my_coup = RemoteCoup('pi','10.0.10.200')
# print('coup status: {}'.format(my_coup.status))
# my_coup.set_light_mode('LIGHT_MODE.PRE_BED.value')
# print('coup status: {}'.format(my_coup.status))
# my_coup.set_light_mode('LIGHT_MODE.ALL_OFF.value')
# print('coup status: {}'.format(my_coup.status))
# my_coup.set_light_mode('LIGHT_MODE.ALL_ON.value')
# print('coup status: {}'.format(my_coup.status))

# my_coup.session.interact()