from . import home_dir, cache_dir, save_object, load_object

import re, pexpect, logging, http.client, csv, datetime, os, json
from pathlib import Path

logger = logging.getLogger(__name__)

OUI_CACHE = 'oui.pickle'
DEVICE_CACHE = 'devices.pickle'

class network_references:
    SERVER_SOURCE = 'standards-oui.ieee.org'
    DOCS = {
        'oui': '/oui/oui.csv',
        'mam': '/oui28/mam.csv',
        'oui36': '/oui36/oui36.csv',
        'cid': '/cid/cid.csv',
        'ethtype': '/ethertype/eth.csv',
        'mid': '/manid/manid.csv',
        'oid': '/bopid/opid.csv',
        'iab': '/iab/iab.csv'
    }

    ouis = None

    def __init__(self):
        logger.info("Initializing network references")

        logger.info("Getting OUI mappings")
        oui_cache = cache_dir / OUI_CACHE
        if oui_cache.exists():
            logger.info('{0} exists so loading OUI map from cache'.format(oui_cache))
            self.ouis = load_object(oui_cache)
            logger.info('OUI map loaded from cache')
        else:
            logger.info('{0} missing so loading OUI map from {1}'.format(oui_cache, self.SERVER_SOURCE))
            self.load_ouis()
            logger.info('OUI map loaded from {0}, caching to {1}'.format(self.SERVER_SOURCE, oui_cache))
            save_object(self.ouis, oui_cache)
            logger.info('OUI map cached to {0}'.format(oui_cache))

    def _load_csv(self, doc_name):
        conn = http.client.HTTPConnection(self.SERVER_SOURCE)
        conn.request('GET',self.DOCS[doc_name])
        lines = (line.decode('utf-8') for line in conn.getresponse())
        csv_reader = csv.reader(lines, delimiter=',', quotechar='"')
        entries = []
        headers = next(csv_reader)
        for row in csv_reader:
            entry = {}
            for index in range(len(headers)):
                entry[headers[index]] = row[index]
            entries.append(entry)
        return entries

    def load_ouis(self):
        logger.info('Starting OUI load')
        self.ouis = {}
        for entry in self._load_csv('oui'):
            self.ouis[entry['Assignment']] = entry
        logger.info('Finished OUI load')

class arp_device:
    # gateway.home (10.0.10.1) at 18:9c:27:88:5a:10 on en0 ifscope [ethernet]
    # matcher = re.compile('([^ ]+) \(([^\(]+)\) at ([^ ]+) on ([^ ]+) ifscope \[([^\]])\]')
    matcher = re.compile('([^ ]+) \(([^\(]+)\) at ([^ ]+) on ([^ ]+)( ifscope)?( permanent)? \[([^\]]+)\]')
    def __init__(self, arp_string, net_ref):
        match = self.matcher.fullmatch(arp_string)
        if match is None:
            logger.info('No match for ' + arp_string)
            # Might need to throw exception
        else:
            self.arp_string = arp_string
            self.name = match.group(1)
            self.ip = match.group(2)
            self.mac_string = match.group(3)
            self.mac = mac_to_hex(self.mac_string) if self.mac_string != '(incomplete)' else None
            self.manufacturer = net_ref.ouis[self.mac[:6]]['Organization Name'] if ((self.mac is not None) and (self.mac[:6] in net_ref.ouis)) else None
            self.interface = match.group(4)
            self.ifscope = (match.group(5) is not None)
            self.permanent = (match.group(6) is not None)
            self.net_type = match.group(7)

    def __str__(self):
        return '{7}: {0} ({1}) = {2}, if={3}, ifscope={4}, static={5}, type={6}'.format(
            self.name, self.ip, self.mac, self.interface, self.ifscope, self.permanent, self.net_type, self.manufacturer)

class finder:
    ARP_NAMES = 'arp -a'
    ARP_IPS = 'arp -an'

    net_ref = network_references()
    manufacturer_map = {}

    def __init__(self):
        device_cache = cache_dir / DEVICE_CACHE
        if device_cache.exists():
            logger.info('Loading devices from {}'.format(device_cache))
            self.manufacturer_map = load_object(device_cache)
        else:
            self.reload_arp_report()
            logger.info('Caching devices to {}'.format(device_cache))
            save_object(self.manufacturer_map, device_cache)

    def reload_arp_report(self):
        logger.info('Loading ARP report using "{0}"'.format(self.ARP_NAMES))
        lines = pexpect.run(self.ARP_NAMES).decode('utf-8').split('\r\n')
        logger.info('"{0}" completed'.format(self.ARP_NAMES))
        devices = []
        for line in lines:
            logger.debug('Processing line {0}'.format('line'))
            if not len(line): continue
            logger.debug('loading device {} from {}'.format(len(devices), line))
            device = arp_device(line, self.net_ref)
            devices.append(device)
            logger.debug('Processed as {0}'.format(device))
        self.manufacturer_map = {}
        for device in devices:
            manufacturer = device.manufacturer
            if manufacturer not in self.manufacturer_map:
                logger.debug('New manufacturer entry of {0}'.format(manufacturer))
                self.manufacturer_map[manufacturer] = []
            logger.debug('Adding {0} to list {1}'.format(device, manufacturer))
            self.manufacturer_map[manufacturer].append(device)
        logger.debug('Loaded device map as {}'.format(self.manufacturer_map))
        return len(devices)

def mac_to_hex(mac_string):
    return '{0:0>2}{1:0>2}{2:0>2}{3:0>2}{4:0>2}{5:0>2}'.format(*mac_string.split(':')).upper()