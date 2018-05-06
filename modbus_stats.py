from mod.mb import Modbus
from mod import utils
import socket
import datetime

import dpkt
import os
import sys

O_PATH = "venv/data/merged/Modbus/"
N_PATH = "venv/data/short/"


TMPFILE = "venv/data/merged/Modbus/3.pcap"
FILE_MAX_SIZE = 500*1024*1024 # in Bytes : 500MB

# stat = utils.Stats()


def new_file(filename):
    writer = dpkt.pcap.Writer(open(N_PATH + str(filename)+".pcap", 'wb'))
    return writer


def update_stats(packet, timestamp, direction, stat):
    """
    Checks give modbus packet propierties, and updates the statistics
    :param packet:
    :param timestamp:
    :param direction:
    :param stat:
    :return:
    """
    mb_pkt = Modbus(packet.data.data.data, timestamp)
    code = mb_pkt.get_code()
    size = mb_pkt.get_size()    # Modbus data size in Bytes
    stat.add_code(code, timestamp, size, direction)

def main():
    create_new_caps = False
    files = os.listdir(O_PATH)
    nn_file = 1
    w_bytes = 0
    if create_new_caps:
        file_writter = new_file(nn_file)

    for f in files:     # Analize all files in current directory
        hosts = []
        stats_array = []
        print(O_PATH + f)
        pcap = dpkt.pcap.Reader(open(O_PATH + f, 'rb'))
        i = True

        for ts, buf in pcap:  # All packets are supposed to be Modbus
            if i:
                print("First packet timestamp: " + str(datetime.datetime.fromtimestamp(ts / 1e3)))
                i = False
            pkg = dpkt.ethernet.Ethernet(buf)

            # Check ip layer
            ip = pkg.data
            # cast ip address to string format
            srce_address = socket.inet_ntoa(ip.src)

            # Define a direction by source ip address
            if srce_address not in hosts:
                hosts.append(srce_address)
                # Itialize statistics for each host
                stats_array.append(utils.Stats(src=srce_address))
            # set up direction and save.
            direction = hosts.index(srce_address)
            stat = stats_array[direction]

            # Do not create too large pcap files.
            if create_new_caps:
                if w_bytes > FILE_MAX_SIZE:
                    file_writter.close()
                    nn_file = nn_file + 1
                    file_writter = new_file(nn_file)
                    w_bytes = 0
                    for a in stats_array:
                        # Show stats for created file
                        a.show()
            try:
                update_stats(pkg, ts, direction, stat)
            except Exception as ex:
                continue
            if create_new_caps:
                file_writter.writepkt(pkg, ts)
                w_bytes = w_bytes + len(buf) + sys.getsizeof(ts)

        print("Last packet timestamp: " + str(datetime.datetime.fromtimestamp(ts / 1e3)))
        # Append stats to file for each 'big' capture file
        stat.to_file()




main()
