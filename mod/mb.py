import dpkt

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
        self.hosts_mac_addr = []
        self.hosts_ip_addr = []
        self.hosts_so = []
        # self.hosts_timestamp = []
        self.hosts_ports = []
        self.hosts_services = []

    def add_mac_addr(self, host1, host2=None):
        if host1 not in self.hosts_mac_addr:
            self.hosts_mac_addr.append(host1)

        if type(host2) != (type(None)) and host2 not in self.hosts_mac_addr:
            self.hosts_mac_addr.append(host2)

    def add_ip_addr(self, host1, host2=None):
        if host1 not in self.hosts_ip_addr:
            self.hosts_ip_addr.append(host1)

        if type(host2) != (type(None)) and host2 not in self.hosts_ip_addr:
            self.hosts_ip_addr.append(host2)



    def show(self):
        print(self.hosts_mac_addr)
        print(self.hosts_ip_addr)