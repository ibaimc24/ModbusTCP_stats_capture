from mod.mb import Modbus
from mod import utils
from mod.utils import Stats
import socket
import datetime

import dpkt
import os
import sys

# Path to Modbus files
O_PATH = "venv/data/merged/Modbus/"

# Path to new files
N_PATH = "venv/data/short/"

# Flag to debug
DEBUG = True

# Flag to create new capture files or only analyze
DIVIDE = True

# Flag to ignore retransmitted TCP packets
# IGNORE_RTX = True

TMPFILE = "venv/data/merged/Modbus/3.pcap"
FILE_MAX_SIZE = 500*1024*1024  # in Bytes : 500MB

# stat = utils.Stats()


def new_file(old_file_number, new_file_number):
    writer = dpkt.pcap.Writer(open(N_PATH + str(old_file_number)+"_"+str(new_file_number)+".pcap", 'wb'))
    return writer


def update_stats(packet, timestamp, direction, stat):
    """
    Checks given modbus packet propierties, and updates the statistics
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
    # Get files from given path
    files = os.listdir(O_PATH)

    # counter to new files names
    new_file_number = 1

    # Written bytes in new capture file
    w_bytes = 0

    # counter that indicates current old file capture number
    old_file_number = 1

    # Variable for last packet timestamp of each pcap file
    last_ts = None

    file_writer = new_file(old_file_number, new_file_number)
    for f in files:     # Analyze all files in current directory
        # Hosts IP Addresses involved in MODBUS communication
        hosts = []

        # Statistics objects array in same indexes of hosts array
        stats_array = []
        print(O_PATH + f)
        pcap = dpkt.pcap.Reader(open(O_PATH + f, 'rb'))
        i = True

        for ts, buf in pcap:  # All packets are supposed to be Modbus
            if i and DEBUG:
                print("First packet timestamp: " + str(datetime.datetime.fromtimestamp(ts / 1e3)))
                i = False
            # Create packet from raw
            pkg = dpkt.ethernet.Ethernet(buf)

            # Check ip layer
            ip = pkg.data

            # cast ip address to string format
            source_address = socket.inet_ntoa(ip.src)

            # Define a direction by source ip address if doesnt exist
            if source_address not in hosts:
                hosts.append(source_address)
                # Initialize statistics for each host
                stats_array.append(utils.Stats(src=source_address))

            # Check packet direction and get 'Stat' object
            direction = hosts.index(source_address)
            stat = stats_array[direction]

            # noinspection PyBroadException
            try:
                # Save stats of the current packet with given information in 'stats' object
                update_stats(pkg, ts, direction, stat)
            except Exception:
                continue

            # Saving into new files
            if DIVIDE:
                # Check if new file is too large and create new file
                if w_bytes > FILE_MAX_SIZE:
                    file_writer.close()
                    new_file_number = new_file_number + 1
                    file_writer = new_file(old_file_number, new_file_number)
                    w_bytes = 0
                    if DEBUG:
                        for a in stats_array:
                            # Show stats for created file
                            a.show()

                # Write packet and timestamp in new file
                file_writer.writepkt(pkg, ts)
                # Update written bytes in new file
                w_bytes = w_bytes + len(buf) + sys.getsizeof(ts)
                last_ts = ts

        if DEBUG:
            print("Last packet timestamp: " + str(datetime.datetime.fromtimestamp(last_ts / 1e3)))
        # Append stats to file for each old capture file
        Stats.to_file(stats_array)
        del hosts
        del stats_array
        old_file_number += 1


if __name__ == "__main__":
    main()
