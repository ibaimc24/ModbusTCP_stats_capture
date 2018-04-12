import sys
import dpkt

#MODBUS FUNCTION CODES:
MOD_READ_COIL = 1
MOD_READ_DISC_IN = 2

# 250V 200ma

def main():

    for i in range(1,7):

        modbus_packets = 0
        no_modbus_packets = 0


        filename = ("throwingstarpi-b-capture_" +str(i)+".pcap")
        print("Processing new file: " +filename)
        pcap = dpkt.pcap.Reader(open("old_data/"+filename,'rb'))
        writer = dpkt.pcap.Writer(open("new_data/"+filename,'wb'))
        rub = dpkt.pcap.Writer(open("rubbish_data/rub_"+filename, 'wb'))
        exc = dpkt.pcap.Writer(open("excpt.pcap", 'wb'))
        #writer = dpkt.pcap.Writer(open("Test3.pcap", 'wb'))
        try:
            for ts,buf in pcap:
                if len(buf)>16: #broken packets
                    try:
                        pkg = dpkt.ethernet.Ethernet(buf)
                    except:
                        print("failed in line 18 with exception")
                        continue

                    if pkg.type==dpkt.ethernet.ETH_TYPE_IP: # CHeck if IP
                        ip_pkg = pkg.data
                        try:
                            if ip_pkg.p==dpkt.ip.IP_PROTO_TCP and (ip_pkg.data.sport==502 or ip_pkg.data.dport==502 ) and ((ip_pkg.data.flags & dpkt.tcp.TH_PUSH)!=0): #Check if modbus by port and PUSH flag
                                '''
                                # MODBUS PACKET
                                tcp_pkg = ip_pkg.data
                                modbus_pkg = tcp_pkg.data
                                function_code = modbus_pkg[7]
                                if function_code is MOD_READ_COIL:
                                    
                                # Modbus statistics
                                '''
                                writer.writepkt(pkg,ts)
                                modbus_packets = modbus_packets + 1
                            else:
                                rub.writepkt(pkg,ts)
                                no_modbus_packets = no_modbus_packets + 1
                        except:
                            exc.writepkt(pkg,ts)
                            continue

                    else:
                        rub.writepkt(pkg,ts)
                        no_modbus_packets = no_modbus_packets + 1

                else:
                    continue
        except:
            print("Yolo")
            continue

        wf = open(filename+".log",'w')
        wf.write("Modbus Packets: "+str(modbus_packets))
        wf.write("No Modbus Packets: " + str(no_modbus_packets))
        wf.close()


main()
