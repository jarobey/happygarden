import piplates.RELAYplate as RELAY
import json, logging
from enum import Enum

logger = logging.getLogger(__name__)

class LIGHT_MODE(Enum):
    ALL_ON = """{"Coup": {"Lights": {"Run Light 1": true , "Run Light 2": true , "Coup Light 1": true, "Coup Light 2": true}}}"""
    PRE_BED = """{"Coup": {"Lights": {"Run Light 1": false, "Run Light 2": false, "Coup Light 1": false, "Coup Light 2": false}}}"""
    ALL_OFF = """{"Coup": {"Lights": {"Run Light 1": true , "Run Light 2": false, "Coup Light 1": false, "Coup Light 2": false}}}"""

class Coup():
    relay_plate_id = 0
    light_names = ['Run Light 1', 'Run Light 2', 'Coup Light 1', 'Coup Light 2']

    coup_dict = {'Coup': 
    {
        'Lights': {}, 
        'Doors': {}, 
        'Temperatures': {}, 
        'Plate Status': {}, 
        'LEDs': {'Relay Plate {} LED'.format(relay_plate_id): False}
    }}
    RELAY.clrLED(relay_plate_id)

    def get_status(self):
        relay_state = RELAY.relaySTATE(self.relay_plate_id)
        self.coup_dict['Coup']['Plate Status'] = relay_state
        i = 0
        status = {}
        for light_name in self.light_names:
            status[light_name] = pow(2, i) & relay_state > 0
            i += 1
        self.coup_dict['Coup']['Lights'] = status
        return json.dumps(self.coup_dict)

    # TODO: Invert state to only check passed in state--take away requirement to pass in fully built json state    
    def set_state(self, desired_state_json):
        desired_state = json.loads(desired_state_json)
        current_state = json.loads(self.get_status())
        lights = current_state['Coup']['Lights']
        for light, state in lights.items():
            if state != desired_state['Coup']['Lights'][light]:
                self.set_light(light, desired_state['Coup']['Lights'][light])

    def set_light(self, name, value):
        light = self.light_names.index(name) + 1
        if value:
            RELAY.relayON(self.relay_plate_id, light)
        else:
            RELAY.relayOFF(self.relay_plate_id, light)

    def set_light_mode(self, mode):
        self.set_state(mode)

# c = Coup()
# c.set_state('{"Coup": {"Lights": {"Coup Light 2": true, "Run Light 2": true, "Coup Light 1": true, "Run Light 1": false}, "Doors": {}, "Temperatures": {}}}')