from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
from pyhap.const import CATEGORY_LIGHTBULB
import logging, signal
from .coup import RemoteCoup

class RemoteGardenLight(Accessory):
    """Remoting RaspberryPi from AHK Hub on server"""

    category = CATEGORY_LIGHTBULB
    name = None
    coup = None

    def __init__(self, *args, name, coup, **kwargs):
        super().__init__(*args, display_name=name, **kwargs)

        light_service = self.add_preload_service('Lightbulb')
        self.char_on = light_service.configure_char('On', setter_callback=self.set_runlight)
        self.name = name

    def set_runlight(self, value):
        self.coup['Coup']['Lights'][self.name] = value
        self.coup.set_desired_state(self.coup.status)

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
    coup = None
    
    def __init__(self, hub_name, user, device):
        logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

        # Initialize my coup
        self.hub_name = hub_name
        coup = RemoteCoup(user, device)
        
        # Start the accessory on port 51826
        self.driver = AccessoryDriver(port=51826)

        self.bridge = Bridge(self.driver, self.hub_name)

        # Setup run and coup lights
        for light in coup.status['Coup']['Lights']:
            print(light)
            runlight = RemoteGardenLight(self.driver, name=light, coup=coup)
            self.bridge.add_accessory(runlight)
        
        # Change `get_accessory` to `get_bridge` if you want to run a Bridge.
        self.driver.add_accessory(accessory=self.bridge)

        # We want SIGTERM (terminate) to be handled by the driver itself,
        # so that it can gracefully stop the accessory, server and advertising.
        signal.signal(signal.SIGTERM, self.driver.signal_handler)

    def start(self):
        self.driver.start()