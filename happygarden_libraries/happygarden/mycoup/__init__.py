import piplates.RELAYplate as RELAY
import json

class Coup():
    relay_plate_id = 0
    light_names = ['Run Light 1', 'Run Light 2', 'Coup Light 1', 'Coup Light 2']
    coup_dict = {'Coup': {'Lights': {}, 'Doors': {}, 'Temperatures': {}, 'Plate Status': {}}}
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
    def set_light(self, name, value):
        # print('Setting {0} to {1} for value {2}'.format(name, 'On' if value else 'Off', value))
        light = self.light_names.index(name) + 1
        if value:
            # print('Calling relayON for plate {0}, relay {1} a.k.a. {2}'.format(self.relay_plate_id, light, name))
            RELAY.relayON(self.relay_plate_id, light)
        else:
            # print('Calling relayOFF for plate {0}, relay {1} a.k.a. {2}'.format(self.relay_plate_id, light, name))
            RELAY.relayOFF(self.relay_plate_id, light)
    def set_state(self, desired_state_json):
        desired_state = json.loads(desired_state_json)
        current_state = json.loads(self.get_status())
        lights = current_state['Coup']['Lights']
        for light, state in lights.items():
            if state != desired_state['Coup']['Lights'][light]:
                self.set_light(light, desired_state['Coup']['Lights'][light])

# c = Coup()
# c.set_state('{"Coup": {"Lights": {"Coup Light 2": true, "Run Light 2": true, "Coup Light 1": true, "Run Light 1": false}, "Doors": {}, "Temperatures": {}}}')
