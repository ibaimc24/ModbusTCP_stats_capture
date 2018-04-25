from mod.mb import Modbus
from mod import utils
import socket

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
    mb_pkt = Modbus(packet.data.data.data, timestamp)
    code = mb_pkt.get_code()
    size = mb_pkt.get_size()    # Modbus data size in Bytes
    #stat.new_pkt(timestamp)
    stat.add_code(code, timestamp, size, direction)

def main():
    hosts = []
    files = os.listdir(O_PATH)
    stats_array = []

    nn_file = 1
    w_bytes = 0
    file_writter = new_file(nn_file)

    for f in files:
        print(O_PATH + f)
        # pcap = dpkt.pcap.Reader(open(O_PATH+f, 'rb'))
        pcap = dpkt.pcap.Reader(open(O_PATH + f, 'rb'))

        for ts, buf in pcap: #All packets are supposed to be Modbus

            pkg = dpkt.ethernet.Ethernet(buf)

            ip = pkg.data
            srce_address = socket.inet_ntoa(ip.src)
            if srce_address not in hosts:       # Define a direction by source ip address
                hosts.append(srce_address)
                stats_array.append(utils.Stats(src=srce_address))
            direction = hosts.index(srce_address)
            stat = stats_array[direction]

            if w_bytes > FILE_MAX_SIZE:
                file_writter.close()
                nn_file = nn_file + 1
                file_writter = new_file(nn_file)
                w_bytes = 0
                for a in stats_array:
                    print("BP")
                    a.show()
            try:
                update_stats(pkg, ts, direction, stat)
            except Exception as ex:
                continue
            file_writter.writepkt(pkg, ts)
            w_bytes = w_bytes + len(buf) + sys.getsizeof(ts)
        stat.to_file()




main()
