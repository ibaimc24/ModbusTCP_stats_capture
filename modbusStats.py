from mod.mb import Modbus
from mod import utils

import dpkt
import os
import sys

O_PATH = "venv/data/merged/Modbus/"
N_PATH = "venv/data/short/"


TMPFILE = "venv/data/merged/Modbus/3.pcap"
FILE_MAX_SIZE = 10*1024*1024 # in Bytes : 500MB

stat = utils.Stats()

def newFile(filename):
    writer = dpkt.pcap.Writer(open(N_PATH + str(filename)+".pcap", 'wb'))
    return writer

def updateStats(packet,timestamp):
    mb_pkt = Modbus(packet.data.data.data, timestamp)
    code = mb_pkt.get_code()
    size = mb_pkt.get_size() # Modbus data size in Bytes
    #stat.new_pkt(timestamp)
    stat.add_code(code, timestamp, size)

def main():
    files = os.listdir(O_PATH)

    nn_file = 1
    w_bytes = 0
    file_writter = newFile(nn_file)

    for f in files:
        print(O_PATH + f)
        #pcap = dpkt.pcap.Reader(open(O_PATH+f, 'rb'))
        pcap = dpkt.pcap.Reader(open(TMPFILE, 'rb'))

        for ts, buf in pcap: #All packets are supposed to be Modbus
            pkg = dpkt.ethernet.Ethernet(buf)
            if w_bytes > FILE_MAX_SIZE:
                stat.show()
                stat.to_file()
                file_writter.close()
                exit(3)
                nn_file = nn_file + 1
                file_writter = newFile(nn_file)
                w_bytes = 0

            updateStats(pkg, ts)
            file_writter.writepkt(pkg,ts)
            w_bytes = w_bytes + len(buf) + sys.getsizeof(ts)




main()
