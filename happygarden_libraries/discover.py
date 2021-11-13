import time, logging
from happygarden.discover import finder
import wemo

logger = logging.getLogger(__name__)

WEMO_MANU = 'Belkin International Inc.'

finder = finder()
for manufacturer, device_list in finder.manufacturer_map.items():
    logger.info("{0}".format(manufacturer))
    device_num = 1
    for device in device_list:
        logger.info('  {0}) {1}'.format(device_num, device))
        device_num += 1

wemos = []
if WEMO_MANU in finder.manufacturer_map:
    logger.info('Loading {0} devices'.format(WEMO_MANU))
    for wemo_device in finder.manufacturer_map[WEMO_MANU]:
        logger.debug('Loading {0}'.format(wemo_device))
        wemos.append(wemo.switch(wemo_device.ip))
        logger.debug('Loaded {0}'.format(wemo_device))

while True:
    for wemo_device in wemos:
        print('{0}: {1}'.format(wemo_device.name, wemo_device.status()))
    time.sleep(10)