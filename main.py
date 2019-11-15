"""An example of how to setup and start an Accessory.
This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal
import random

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
#from pyhap import camera
from runlight import GardenLight
#from PiCamV2 import cameraOptions

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")



def get_bridge(driver):
    bridge = Bridge(driver, 'Bridge')

    # Setup run and coup lights
    runlight1 = GardenLight(driver, 'Run Light 1', relay=1)
    runlight2 = GardenLight(driver, 'Run Light 2', relay=2)
    couplight1 = GardenLight(driver, 'Coup Light 1', relay=3)
    couplight2 = GardenLight(driver, 'Coup Light 2', relay=4)
    bridge.add_accessory(runlight1)
    bridge.add_accessory(runlight2)
    bridge.add_accessory(couplight1)
    bridge.add_accessory(couplight2)

    # Setup the Camera
    # camv2 = camera.Camera(cameraOptions, driver, "Run Camera")
    # bridge.add_accessory(camv2)

    return bridge

# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)

# Change `get_accessory` to `get_bridge` if you want to run a Bridge.
driver.add_accessory(accessory=get_bridge(driver))

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()
