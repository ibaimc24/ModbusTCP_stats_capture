import socket
import sys
import dpkt
from mod.mb import NetData

from dpkt.compat import compat_ord
import ipaddress

CHECK_HOSTS = False
nd = NetData()

# Layer levels
LEVEL_MAC = 2
LEVEL_IP = 3
LEVEL_TCP = 4
LEVEL_APLICATION = 5


def mac_addr(address):
    """
    Casts ip raw in string format
    :param address:
    :return:
    """

    return ':'.join('%02x' % compat_ord(b) for b in address)


def inet_to_str(inet):
    """
    Casts ipv4 or ipv6 raw in string format
    :param inet:
    :return:
    """
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


def check_ip_address(pkt):
    if pkt.type == dpkt.ethernet.ETH_TYPE_IP:
        ip_pkt = pkt.data
        nd.add_ip_addr(inet_to_str(ip_pkt.src))


def check_tcp(pkt):
    # noinspection PyBroadException
    try:
        transport = pkt.data.data
        if type(transport) == dpkt.tcp.TCP:
            src_port = transport.sport
            dst_port = transport.dport
            if src_port < 1025:
                nd.add_used_port(src_port, "TCP")
            if dst_port < 1025:
                nd.add_used_port(dst_port, "TCP")
        elif type(transport) == dpkt.udp.UDP:
            src_port = transport.sport
            dst_port = transport.dport
            if src_port < 1025:
                nd.add_used_port(src_port, "UDP")
            if dst_port < 1025:
                nd.add_used_port(dst_port, "UDP")
    except AttributeError:      # Ignore packet if has no transport Layer
        return


def check_top_proto(pkt):
    level = LEVEL_MAC
    try:
        if isinstance(pkt.data, dpkt.ip.IP):  # Is IP
            level = LEVEL_IP
        if isinstance(pkt.data.data, dpkt.tcp.TCP):
            level = LEVEL_TCP
        level = LEVEL_APLICATION
    except AttributeError:      # Found top level protocol
        return level
    return level


def mac_level(pkt):  # Analyze MAC Level packet like ARP
    """
    Has no IP Layer, so SOURCE and DESTINATION belongs to private network.
    Analyzed protocols:
        None
    :return:
    """
    src_mac = mac_addr(pkt.src)
    dst_mac = mac_addr(pkt.dst)
    nd.add_mac_addr(src_mac)
    nd.add_mac_addr(dst_mac)
    return src_mac, dst_mac


def ip_level(pkt):
    """
    Checks ip layer propierties of the given packet. Saves only private network hosts information filtering by
    source or destination mac address.
    :param pkt:
    :return:
    """
    [src_mac, dst_mac] = mac_level(pkt)
    ip_pkt = pkt.data
    if isinstance(ip_pkt, dpkt.ip.IP):
        next_proto = ip_pkt.p
        # MOST USED:
        # - 6: TCP
        # - 17: UDP
        # - 1: ICMP
        ip_src_addr = inet_to_str(ip_pkt.src)
        ip_dst_addr = inet_to_str(ip_pkt.dst)

        # If source ip address is private, packet sender is in current network
        if ipaddress.ip_address(ip_src_addr).is_private:
            nd.add_ip_addr(src_mac, ip_src_addr)

        # If source ip address is private, packet receiver is in current network
        if ipaddress.ip_address(ip_dst_addr).is_private:
            nd.add_ip_addr(dst_mac, ip_dst_addr)
        return ip_src_addr, ip_dst_addr, next_proto
    elif isinstance(ip_pkt, dpkt.llc.LLC):
        nd.add_used_protocols(src_mac, "LLC")
        nd.add_used_protocols(dst_mac, "LLC")
        return None, None, None


def tcp_level(pkt):
    """
    Checks transport layer propierties of the given packet. Saves only private network hosts information filtering by
    source or destination mac address.
    :param pkt:
    :return:
    """
    # noinspection PyBroadException
    try:
        [src_mac, dst_mac] = mac_level(pkt)
        [ip_src_addr, ip_dst_addr, next_proto] = ip_level(pkt)
    except Exception:
        return

    # noinspection PyBroadException
    try:
        if (next_proto is 6) or (next_proto is 17):     # TCP or UDP
            tcp_pkt = pkt.data.data
            src_port = tcp_pkt.sport
            dst_port = tcp_pkt.dport

            # If source ip address is private, packet sender is in current network. Store only most used service ports
            if ipaddress.ip_address(
                    ip_src_addr).is_private and src_port < 1024:
                nd.add_used_port(src_mac, src_port)
                # Alanize Application layer
                try:
                    application_level(src_mac, tcp_pkt.data)
                except AttributeError:
                    pass

            # If destination ip address is private, packet receiver is in current network.
            # Store only most used service ports
            if ipaddress.ip_address(ip_dst_addr).is_private and dst_port < 1024:
                nd.add_used_port(dst_mac, dst_port)
                # Alanize Application layer
                try:
                    application_level(dst_mac, tcp_pkt.data)
                except AttributeError:
                    pass

        elif next_proto is 1:  # ICMP
            tcp_pkt = pkt.data.data
            if ipaddress.ip_address(
                    ip_src_addr).is_private:  # If source ip address is private, packet sender is in current network
                # Alanize Application layer
                try:
                    application_level(src_mac, tcp_pkt.data)
                except AttributeError:
                    pass
            if ipaddress.ip_address(ip_dst_addr).is_private:
                # Alanize Application layer
                try:
                    application_level(dst_mac, tcp_pkt.data)
                except AttributeError:
                    pass

        elif next_proto is 112:
            pass
    except Exception:
        print(next_proto)


def is_dns(pkt):
    """
    Checks if a packets is DNS message
    :param pkt:
    :return:
    """
    # noinspection PyBroadException
    try:
        dpkt.dns.DNS(pkt)
        return True
    except Exception:
        return False


def is_tls(pkt):
    """
    Checks if a packets is TLS message
    :param pkt:
    :return:
    """
    # noinspection PyBroadException
    try:
        dpkt.ssl.TLS(pkt)
        return True
    except Exception:
        return False


def is_http(pkt):
    """
    Checks if a packets is HTTP message
    :param pkt:
    :return:
    """
    # noinspection PyBroadException
    try:
        dpkt.http.Message(pkt)
        return True
    except Exception:
        return False


def is_icmp(pkt):
    """
    Checks if a packets is ICMP message
    :param pkt:
    :return:
    """
    # noinspection PyBroadException
    try:
        dpkt.icmp.ICMP(pkt)
        return True
    except Exception:
        return False


def application_level(host, pkt):
    if is_tls(pkt):
        nd.add_used_protocols(host, "TLS")
    elif is_dns(pkt):
        nd.add_used_protocols(host, "DNS")
    elif is_http(pkt):
        nd.add_used_protocols(host, "HTTP")
    elif is_icmp(pkt):
        nd.add_used_protocols(host, "ICMP")


switcher = {
    2: mac_level,
    3: ip_level,
    4: tcp_level,
    5: tcp_level
}


def check_source(pkt):
    # check top level protocol
    proto = check_top_proto(pkt)
    func = switcher.get(proto, lambda: "Invalid Level")
    func(pkt)
    return None, None, proto


def main():
    file_name = sys.argv[1]
    pcap = dpkt.pcap.Reader(open(file_name, 'rb'))
    for ts, buf in pcap:
        pkt = dpkt.ethernet.Ethernet(buf)
        # check source
        check_source(pkt)
        check_top_proto(pkt)

    nd.show(file_name.replace(".pcap", ".log"))


if __name__ == "__main__":
    main()
