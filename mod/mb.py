import dpkt
from collections import defaultdict
import json

class Modbus:

    def __init__(self,pkt,ts):
        self.__raw__ = pkt
        self.__ts__ = ts
        self.__size__ = len(pkt)
        self.__update__()

    def __update__(self):
        self.__code__ = self.__raw__[7]

    def get_code(self):
        return self.__code__

    def get_size(self):
        return self.__size__


class NetData:

    def __init__(self):
        self.hosts = {}

    def add_mac_addr(self, host):
        if host not in self.hosts:
            self.hosts[host] = {'ip_address': None, 'protocols':[], 'used_ports':[]}

    def add_ip_addr(self, host, ip):
        if host not in self.hosts:
            self.add_mac_addr(host)
        if ip not in self.hosts[host]:
            self.hosts[host]['ip_address'] = ip
        else:
            print("IP FOUND")

    def add_used_port(self, host, port):
        if host not in self.hosts:
            self.add_mac_addr(host)
        if port not in self.hosts[host]['used_ports']:
            self.hosts[host]['used_ports'].append(port)

    def add_used_protocols(self, host, protocol):
        if host not in self.hosts:
            self.add_mac_addr(host)
        if protocol not in self.hosts[host]['protocols']:
            self.hosts[host]['protocols'].append(protocol)

    def show(self, filename=None):
        j = {'hosts': self.hosts}
        result = json.dumps(j, sort_keys=True, indent=4)
        if filename is None:
            print(result)
        else:
            fp = open(filename, 'w')
            print(result, file=fp)
            fp.close()

