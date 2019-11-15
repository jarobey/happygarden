from pyhap.accessory import Accessory
import pyhap.loader as loader
from pyhap.const import CATEGORY_LIGHTBULB
import piplates.RELAYplate as RELAY

class GardenLight(Accessory):
    """Starting implementation on RELAY plates"""

    category = CATEGORY_LIGHTBULB
    RELAY.clrLED(0)

    def __init__(self, *args, relay=1, **kwargs):
        super().__init__(*args, **kwargs)

        light_service = self.add_preload_service('Lightbulb')
        self.char_on = light_service.configure_char('On', setter_callback=self.set_runlight)
        self.relay_runlight = relay
        self.relay_plateid = 0

    def set_runlight(self, value):
        if value:
            RELAY.relayON(self.relay_plateid,self.relay_runlight)
        else:
            RELAY.relayOFF(self.relay_plateid, self.relay_runlight)
