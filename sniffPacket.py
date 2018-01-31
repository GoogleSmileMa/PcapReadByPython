from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP

dpkt = sniff(offline="amazon_1.pcap")
print(dpkt[0][Ether].type)
print(dpkt[0][Ether].proto)
print(dpkt[0][Ether].show())



