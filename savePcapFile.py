import os
from scapy.all import *

pkts = []
count = 0
pcapnum = 0
filename = 'amazon_1.pcap'


def test_dump_file(dump_file):
    print("Testing the dump file...")

    if os.path.exists(dump_file):
        print("dump fie %s found." % dump_file)
        pkts = sniff(offline=dump_file)
        count = 0
        while (count <= 2):
            print("----Dumping pkt:%s----" % dump_file)
            print(hexdump(pkts[count]))
            count += 1
    else:
        print("dump fie %s not found." % dump_file)


def write_cap(x):
    global pkts
    global count
    global pcapnum
    global filename
    pkts.append(x)
    count += 1
    if count == 3:                         # 每3个TCP操作封为一个包（为了检测正确性，使用时尽量增多）</span>
        pcapnum += 1
        pname = "pcap%d.pcap" % pcapnum
        wrpcap(pname, pkts)
        filename = "./pcap%d.pcap" % pcapnum
        test_dump_file(filename)
        pkts = []
        count = 0


if __name__ == '__main__':
    print("Start packet capturing and dumping ...")
    sniff(filter="src net 192.168.1.1", prn=write_cap)  # BPF过滤规则





