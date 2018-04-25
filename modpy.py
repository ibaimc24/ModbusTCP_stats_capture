import socket
import sys
import dpkt
from mod.mb import NetData
from dpkt.compat import compat_ord
from dpkt.udp import UDP

CHECK_HOSTS = False
nd = NetData()


def mac_addr(address):
    return ':'.join('%02x' % compat_ord(b) for b in address)


def inet_to_str(inet):
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


def check_mac_address(pkt):
    src = mac_addr(pkt.src)
    dst = mac_addr(pkt.dst)
    nd.add_mac_addr(src, dst)


def check_ip_address(pkt):
    if pkt.type == dpkt.ethernet.ETH_TYPE_IP:
        ip = pkt.data
        nd.add_ip_addr(inet_to_str(ip.src))


def check_tcp(pkt):
    try:
        trnsprt = pkt.data.data
        if type(trnsprt) == dpkt.tcp.TCP:
            src_port = trnsprt.sport
            dst_port = trnsprt.dport
            if src_port<1025:
                nd.add_used_port(src_port, "TCP")
            if dst_port<1025:
                nd.add_used_port(dst_port, "TCP")
        elif type(trnsprt) == dpkt.udp.UDP:
            src_port = trnsprt.sport
            dst_port = trnsprt.dport
            if src_port<1025:
                nd.add_used_port(src_port, "UDP")
            if dst_port<1025:
                nd.add_used_port(dst_port, "UDP")
    except AttributeError:      # Ignore packet if has no transport Layer
        None



def main():
    file_name = sys.argv[1]
    pcap = dpkt.pcap.Reader(open(file_name, 'rb'))

    for ts, buf in pcap:
        pkt = dpkt.ethernet.Ethernet(buf)
        check_mac_address(pkt)
        check_ip_address(pkt)
        check_tcp(pkt)
    nd.show()



if __name__ == "__main__":
    main()