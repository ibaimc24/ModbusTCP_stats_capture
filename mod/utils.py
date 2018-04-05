from mod.fcodes import *
import datetime

class Stats:

    def __init__(self):
        self.initial_timestamp = None
        self.n_packets = 0

        # FCODE 1 stats
        self.flag_1 = True
        self.flag_2 = True
        self.flag_3 = True
        self.flag_4 = True
        self.flag_15 = True

        self.n_others = 0
        # FCODE 2 stats


        self.switcher = {
            1: self.__1__,
            2: self.__2__,
            3: self.__3__,
            4: self.__4__,
            5: self.__5__,
            6: self.__6__,
            7: self.__7__,
            8: self.__8__,
            11: self.__11__,
            12: self.__12__,
            15: self.__15__,
            16: self.__16__,
            17: self.__17__,
            20: self.__20__,
            21: self.__21__,
            22: self.__22__,
            23: self.__23__,
            24: self.__24__,
            43: self.__43__
        }

    def __1__(self, ts, psize):
        if self.flag_1:             # First iteration
            self.n_1 = 1            # Number of packets
            self.total_difs_1 = 0   # Sum of timestamps of all packets
            self.last_ts_1 = datetime.datetime.fromtimestamp(ts)
            self.psize_1_10 = 0     # Number of packets with 10 Bytes length
            self.psize_1_12 = 0     # Number of packets with 12 Bytes length
            self.psize_1_others = 0   # Number of packets with other Bytes length
            self.initial_ts = datetime.datetime.fromtimestamp(ts)   # To calculate pkts/sec
            self.flag_1 = False
        else:
            self.n_1 += 1
            if psize is 10:
                self.psize_1_10 += 1
            elif psize is 12:
                self.psize_1_12 += 1
            else:
                self.psize_1_others += 1

            dif = datetime.datetime.fromtimestamp(ts) - self.last_ts_1
            self.total_difs_1 += dif.total_seconds()

            if self.n_1 > 2:        # Difference in seconds between 2 packets with same func code
                self.dif_media_1 = self.total_difs_1/(self.n_1 - 1)

            self.last_ts_1 = datetime.datetime.fromtimestamp(ts)

    def __2__(self, ts, psize):
        if self.flag_2:             # First iteration
            self.n_2 = 1            # Number of packets
            self.total_difs_2 = 0   # Sum of timestamps of all packets
            self.last_ts_2 = datetime.datetime.fromtimestamp(ts)
            self.psize_2_10 = 0     # Number of packets with 10 Bytes length
            self.psize_2_12 = 0     # Number of packets with 12 Bytes length
            self.psize_2_others = 0   # Number of packets with other Bytes length
            #self.initial_ts = datetime.datetime.fromtimestamp(ts)   # To calculate pkts/sec
            self.flag_2 = False
        else:
            self.n_2 += 1
            if psize is 10:
                self.psize_2_10 += 1
            elif psize is 12:
                self.psize_2_12 += 1
            else:
                self.psize_2_others += 1

            dif = datetime.datetime.fromtimestamp(ts) - self.last_ts_2
            self.total_difs_2 += dif.total_seconds()

            if self.n_2 > 2:        # Difference in seconds between 2 packets with same func code
                self.dif_media_2 = self.total_difs_2/(self.n_2 - 1)

            self.last_ts_2 = datetime.datetime.fromtimestamp(ts)

    def __3__(self, ts, psize):
        if self.flag_3:             # First iteration
            self.n_3 = 1            # Number of packets
            self.total_difs_3 = 0   # Sum of timestamps of all packets
            self.last_ts_3 = datetime.datetime.fromtimestamp(ts)
            self.psize_3_10 = 0     # Number of packets with 10 Bytes length
            self.psize_3_12 = 0     # Number of packets with 12 Bytes length
            self.psize_3_others = 0   # Number of packets with other Bytes length
            #self.initial_ts = datetime.datetime.fromtimestamp(ts)   # To calculate pkts/sec
            self.flag_3 = False
        else:
            self.n_3 += 1
            if psize is 10:
                self.psize_3_10 += 1
            elif psize is 12:
                self.psize_3_12 += 1
            else:
                self.psize_3_others += 1

            dif = datetime.datetime.fromtimestamp(ts) - self.last_ts_3
            self.total_difs_3 += dif.total_seconds()

            if self.n_3 > 2:        # Difference in seconds between 2 packets with same func code
                self.dif_media_3 = self.total_difs_3/(self.n_3 - 1)

            self.last_ts_3 = datetime.datetime.fromtimestamp(ts)

    def __4__(self, ts, psize):
        if self.flag_4:             # First iteration
            self.n_4 = 1            # Number of packets
            self.total_difs_4 = 0   # Sum of timestamps of all packets
            self.last_ts_4 = datetime.datetime.fromtimestamp(ts)
            self.psize_4_10 = 0     # Number of packets with 10 Bytes length
            self.psize_4_12 = 0     # Number of packets with 12 Bytes length
            self.psize_4_others = 0   # Number of packets with other Bytes length
            #self.initial_ts = datetime.datetime.fromtimestamp(ts)   # To calculate pkts/sec
            self.flag_4 = False
        else:
            self.n_4 += 1
            if psize is 10:
                self.psize_4_10 += 1
            elif psize is 12:
                self.psize_4_12 += 1
            else:
                self.psize_4_others += 1

            dif = datetime.datetime.fromtimestamp(ts) - self.last_ts_4
            self.total_difs_4 += dif.total_seconds()

            if self.n_4 > 2:        # Difference in seconds between 2 packets with same func code
                self.dif_media_4 = self.total_difs_4/(self.n_4 - 1)

            self.last_ts_4 = datetime.datetime.fromtimestamp(ts)


    def __5__(self, ts, psize):
        self.n_others += 1

    def __6__(self, ts, psize):
        self.n_others += 1

    def __7__(self, ts, psize):
        self.n_others += 1

    def __8__(self, ts, psize):
        self.n_others += 1

    def __11__(self, ts, psize):
        self.n_others += 1

    def __12__(self, ts, psize):
        self.n_others += 1

    def __15__(self, ts, psize):
        if self.flag_15:             # First iteration
            self.n_15 = 1            # Number of packets
            self.total_difs_15 = 0   # Sum of timestamps of all packets
            self.last_ts_15 = datetime.datetime.fromtimestamp(ts)
            self.psize_15_10 = 0     # Number of packets with 10 Bytes length
            self.psize_15_12 = 0     # Number of packets with 12 Bytes length
            self.psize_15_others = 0   # Number of packets with other Bytes length
            #self.initial_ts = datetime.datetime.fromtimestamp(ts)   # To calculate pkts/sec
            self.flag_15 = False
        else:
            self.n_15 += 1
            if psize is 10:
                self.psize_15_10 += 1
            elif psize is 12:
                self.psize_15_12 += 1
            else:
                self.psize_15_others += 1

            dif = datetime.datetime.fromtimestamp(ts) - self.last_ts_15
            self.total_difs_15 += dif.total_seconds()

            if self.n_15 > 2:        # Difference in seconds between 2 packets with same func code
                self.dif_media_15 = self.total_difs_15/(self.n_15 - 1)

            self.last_ts_15 = datetime.datetime.fromtimestamp(ts)

    def __16__(self, ts, psize):
        self.n_others += 1

    def __17__(self, ts, psize):
        self.n_others += 1

    def __20__(self, ts, psize):
        self.n_others += 1

    def __21__(self, ts, psize):
        self.n_others += 1

    def __22__(self, ts, psize):
        self.n_others += 1

    def __23__(self, ts, psize):
        self.n_others += 1

    def __24__(self, ts, psize):
        self.n_others += 1

    def __43__(self, ts, psize):
        self.n_others += 1

    def get_stats(self):
        media = self.sum_2/self.n_2
        return media

    def add_code(self, option, ts, psize):
        func = self.switcher.get(option, lambda: "Invalid Code")
        func(ts, psize)

    def to_file(self, filename='venv/log/stats.log'):
        wf = open(filename, 'a')
        print("MODBUS CODE\t | \tN. PACKETS\t | \tTIME BTWEEN PKTS(s)\t | \tPCKT SIZES", file=wf)

        print(str(1) + "\t\t\t | \t\t" + str(self.n_1) + "\t | \t" + str(self.dif_media_1) + "\t | \t[10 Bytes:" + str(
            self.psize_1_10) + ", 12 Bytes:" + str(self.psize_1_12) + ", Other size:" + str(self.psize_1_others) + "]",
              file=wf)

        print(str(2) + "\t\t\t | \t\t" + str(self.n_2) + "\t | \t" + str(self.dif_media_2) + "\t | \t[10 Bytes:" + str(
            self.psize_2_10) + ", 12 Bytes:" + str(self.psize_2_12) + ", Other size:" + str(self.psize_2_others)+ "]",
              file=wf)

        '''
        print(str(3) + "\t\t\t | \t\t" + str(self.n_3) + "\t | \t" + str(self.dif_media_3) + "\t | \t[10 Bytes:" + str(
            self.psize_3_10) + ", 12 Bytes:" + str(self.psize_3_12) + ", Other size:" + str(self.psize_3_others) + "]",
              file=wf)
        
        print(str(4) + "\t\t\t | \t\t" + str(self.n_4) + "\t | \t" + str(self.dif_media_4) + "\t | \t[10 Bytes:" + str(
            self.psize_4_10) + ", 12 Bytes:" + str(self.psize_4_12) + ", Other size:" + str(self.psize_4_others) + "]",
              file=wf)
        '''


        print(str(15) + "\t\t\t | \t\t" + str(self.n_15) + "\t | \t" + str(self.dif_media_15) + "\t | \t[10 Bytes:" + str(
            self.psize_15_10) + ", 12 Bytes:" + str(self.psize_15_12) + ", Other size:" + str(self.psize_15_others) + "]",
              file=wf)


        print("OTHERS: "+str(self.n_others), file=wf)



    '''
        To Update Modbus Packets per second
    '''
    def new_pkt(self, ts):
        self.n_packets += 1
        if self.initial_timestamp is None:
            self.initial_timestamp = datetime.datetime.fromtimestamp(ts)
        else:
            dif = datetime.datetime.fromtimestamp(ts) - self.initial_timestamp
            print("Modbus Packets per second:")
            pps = self.n_packets / (dif.microseconds)
            print(pps)


    def show(self):
        None
        #print("Code 1:" + str(self.n_1) + ":" + str(self.sum_1) + " - Packets per second: " + str(self.n_1 / datetime.datetime.second(self.sum_1)))
        #print("Code 2:" + str(self.n_2) + ":" + str(self.sum_2)+" - Packets per second: "+str(self.n_2/self.sum_2))
        #print("Code 3:" + str(self.n_3) + ":" + str(self.sum_3)+" - Packets per second: "+str(self.n_1/self.sum_1))
        #print("Code 15:" + str(self.n_15) + ":" + str(self.sum_15)+" - Packets per second: "+str(self.n_15/self.sum_15))


