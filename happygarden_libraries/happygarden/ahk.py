from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
from pyhap.const import CATEGORY_LIGHTBULB
import logging, signal

class RemoteGardenLight(Accessory):
    """Remoting RaspberryPi from AHK Hub on server"""

    # category = CATEGORY_LIGHTBULB

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

"""An example of how to setup and start an Accessory.
This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
class GardenHub():
    hub_name = "OfficeIMac"
    driver = None
    bridge = None
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")
        
        # Start the accessory on port 51826
        self.driver = AccessoryDriver(port=51826)

        self.bridge = Bridge(self.driver, self.hub_name)
        # Setup run and coup lights
        runlight1 = GardenLight(driver, 'Run Light 1', relay=1)
        runlight2 = GardenLight(driver, 'Run Light 2', relay=2)
        couplight1 = GardenLight(driver, 'Coup Light 1', relay=3)
        couplight2 = GardenLight(driver, 'Coup Light 2', relay=4)
        self.bridge.add_accessory(runlight1)
        self.bridge.add_accessory(runlight2)
        self.bridge.add_accessory(couplight1)
        self.bridge.add_accessory(couplight2)
        
        # Change `get_accessory` to `get_bridge` if you want to run a Bridge.
        self.driver.add_accessory(accessory=self.bridge)

        # We want SIGTERM (terminate) to be handled by the driver itself,
        # so that it can gracefully stop the accessory, server and advertising.
        signal.signal(signal.SIGTERM, driver.signal_handler)

    def start(self):
        self.driver.start()

hub = GardenHub()
hub.start()