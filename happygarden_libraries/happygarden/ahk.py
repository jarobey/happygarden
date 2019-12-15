from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
from pyhap.const import CATEGORY_LIGHTBULB
import logging, signal
from .coup import RemoteCoup
import time
from datetime import datetime

logger = logging.getLogger(__package__ + __name__)

class RemoteGardenLight(Accessory):
    TIME_OUT = 60 # validate every minute
    category = CATEGORY_LIGHTBULB
    coup = None

    def __init__(self, *args, name, coup, **kwargs):
        super().__init__(*args, display_name=name, **kwargs)

        self.coup = coup
        light_service = self.add_preload_service('Lightbulb')
        self.char_on = light_service.configure_char('On', setter_callback=self.set_runlight, getter_callback=self.get_runlight, value=self.get_runlight())
        logger.info('Added Device: %s',self)
        self.check_time = time.time()

    def set_runlight(self, value):
        # LightBulb-On is a bool characteristic.  AHK may send a 1/0, but it will show as True/False in the characteristic On
        value = bool(value)
        status = self.coup.get_status()
        status['Coup']['Lights'][self.display_name] = value
        self.coup.apply_status(status)
        logger.debug("Set RemoteGardenLight %s to %s", self.display_name, value)

    def get_runlight(self):
        status = self.coup.get_status()
        if status is None: return None
        return status['Coup']['Lights'][self.display_name]

class GardenHub():
    hub_name = None
    driver = None
    bridge = None
    coup = None
    
    def __init__(self, hub_name, user, device, listen_address=None):
        logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

        # Initialize my coup
        self.hub_name = hub_name
        coup = RemoteCoup(user, device)
        
        # Start the accessory on port 51826
        if listen_address: self.driver = AccessoryDriver(port=51826, address=listen_address)
        else: self.driver = AccessoryDriver(port=51826)

        self.bridge = Bridge(self.driver, self.hub_name)

        # Setup run and coup lights
        while True:
            status = coup.get_status()
            if (status is None) or ('Coup' not in status) or ('Lights' not in status['Coup']):
                logger.error("Status has not been initialized or lights missing: Status = {0} at {1}".format(status, datetime.now()))
            else:
                for light in status['Coup']['Lights']:
                    logger.info("Adding %s", light)
                    runlight = RemoteGardenLight(self.driver, name=light, coup=coup)
                    self.bridge.add_accessory(runlight)
                break
            time.sleep(5)
        
        # Change `get_accessory` to `get_bridge` if you want to run a Bridge.
        self.driver.add_accessory(accessory=self.bridge)

        # We want SIGTERM (terminate) to be handled by the driver itself,
        # so that it can gracefully stop the accessory, server and advertising.
        signal.signal(signal.SIGTERM, self.driver.signal_handler)

    def start(self):
        self.driver.start()
        print("Completed {0} start".format(__name__))