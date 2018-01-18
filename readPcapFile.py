from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP


def sniff_data(n, evenpcap, oddpcap, starttime1, endtime1, starttime2, endtime2):
    if n % 2 == 0:
        evenpcap = sniff(offline="206_"+str(n)+".pcap")
        starttime1 = oddpcap[0].time * 1000000
        endtime1 = oddpcap[-1].time * 1000000
        starttime2 = evenpcap[0].time * 1000000
        endtime2 = evenpcap[-1].time * 1000000
    else:
        oddpcap = sniff(offline="206_"+str(n)+".pcap")
        starttime1 = evenpcap[0].time * 1000000
        endtime1 = evenpcap[-1].time * 1000000
        starttime2 = oddpcap[0].time * 1000000
        endtime2 = oddpcap[-1].time * 1000000
    print(str(num) + ":" + str(starttime1) + "," + str(endtime1) + "," + str(starttime2) + "," + str(endtime2))


if __name__ == '__main__':
    evenpcap = sniff(offline="206_0.pcap")
    oddpcap = sniff(offline="206_1.pcap")
    starttime1 = evenpcap[0].time * 1000000
    endtime1 = evenpcap[-1].time * 1000000
    starttime2 = oddpcap[0].time * 1000000
    endtime2 = oddpcap[-1].time * 1000000
    print(str(1) + ":" + str(starttime1) + "," + str(endtime1) + "," + str(starttime2) + "," + str(endtime2))
    for num in range(2, 27):
        if num % 2 == 0:
            evenpcap = sniff(offline="206_" + str(num) + ".pcap")
            starttime1 = oddpcap[0].time * 1000000
            endtime1 = oddpcap[-1].time * 1000000
            starttime2 = evenpcap[0].time * 1000000
            endtime2 = evenpcap[-1].time * 1000000
        else:
            oddpcap = sniff(offline="206_" + str(num) + ".pcap")
            starttime1 = evenpcap[0].time * 1000000
            endtime1 = evenpcap[-1].time * 1000000
            starttime2 = oddpcap[0].time * 1000000
            endtime2 = oddpcap[-1].time * 1000000
        print(str(num) + ":" + str(starttime1) + "," + str(endtime1) + "," + str(starttime2) + "," + str(endtime2))


# endtime = pcap[-1].time*1000000
# w = open('test.txt', 'w')
# with open('147.83.42.206.txt', 'r') as f:
#     for line in f.readlines():
#         # if "youtube" in line:
#         if (int(line.split('#')[1]) <= endtime)and(int(line.split('#')[2]) >= endtime):
#             w.write(line)
# w.close()
# try:
#     #print "[*] OPen new pcap_file %s" % pcap_file
#     sessions=pcap.sessions()
#     for session in sessions:
#         data_payload=""
#         for packet in sessions[session]:
#             try:
#                 data_payload +=str(packet[TCP].payload)
#                 print("[**] Data:%s" % data_payload )
#             except:
#                 pass
# except:
#     print("[*]no pcapfile...")
# print(pcap[-1].time*1000000)
# print(hexdump(pcap[0][Ether]))
# print(hexdump(pcap[0][TCP]))
# print(hexdump(pcap[0][IP]))
