from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP
import readByTime


def sniff_packet(num):
    print("Start to sniff packets...")
    dpkt = sniff(iface="enp3s0", filter="tcp and (src net 10.108.126.3 or dst net 10.108.126.3)", timeout=num)
    # dpkt = sniff(iface="ens33", filter="ip", count=num)
    print("Sniffing packets done")
    return dpkt





if __name__ == "__main__":
    dpkt = sniff_packet(20)
    all_packets = readByTime.cut_packets(dpkt, 10)
    all_flows = readByTime.divide_flow(all_packets)

