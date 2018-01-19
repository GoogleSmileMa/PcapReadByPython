from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP
evenpcap = sniff(offline="amazon_1.pcap")
packettime = 0

print(evenpcap[0][Ether].show)


