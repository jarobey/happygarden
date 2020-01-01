import re, pexpect, logging, http.client, csv

logger = logging.getLogger(__name__)

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
        self.load_ouis()

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
        self.ouis = {}
        for entry in self._load_csv('oui'):
            self.ouis[entry['Assignment']] = entry

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
    ARP_NAMES = "arp -a"

    ip_to_device = {}
    names_to_device = {}
    devices = []
    net_ref = network_references()

    def reload_arp_report(self):
        lines = pexpect.run(self.ARP_NAMES).decode('utf-8').split('\r\n')
        self.ip_to_device.clear()
        self.names_to_device.clear()
        self.devices.clear()
        for line in lines:
            if not len(line): continue
            logger.debug('loading device {} from {}'.format(len(self.devices), line))
            device = arp_device(line, self.net_ref)
            self.devices.append(device)
            self.ip_to_device[device.ip] = device
            if device.name != '?':
                self.names_to_device[device.name] = device
        return len(self.devices)

def mac_to_hex(mac_string):
    print(mac_string.split(':'))
    return '{0:0>2}{1:0>2}{2:0>2}{3:0>2}{4:0>2}{5:0>2}'.format(*mac_string.split(':')).upper()