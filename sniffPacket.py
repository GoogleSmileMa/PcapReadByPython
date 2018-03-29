from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP


if __name__ == '__main__':
    # dpkt = sniff(offline="H:\dataset\TorPcaps\\nonTor\Browsing\SSL_Browsing.pcap")
    dpkt = sniff(offline="amazon_1.pcap")
    print('read is over')
    packet = dpkt[0]
    print(packet[IP].src)
    print(packet[Ether].type)


# dpkt = sniff(offline="H:\dataset\TorPcaps\\nonTor\Browsing\SSL_Browsing.pcap")
# f = open('data.txt', 'w')
# count = 0
# print(dpkt[1].show())
# for packet in dpkt:
#     count = count + 1
#     print(count)
#     ty = packet[Ether].type
#     if ty == 0x800:
#         protocol = packet[Ether].proto
#         srcPort = packet[Ether].sport
#         dstPort = packet[Ether].dport
#         length = packet[Ether].len
#         timetolive = packet[IP].ttl
#         if protocol == 6:
#             window = packet[Ether].window
#         else:
#             window = 0
#         f.write(str(srcPort) + ' ' + str(dstPort) + ' ' + str(length) + ' ' + str(timetolive) + ' ' + str(window) + '\n')
# f.close()
# print(len(dpkt))
# print(dpkt[0][Ether].type)
# print(dpkt[0][Ether].proto)
# print(dpkt[0][Ether].show())



