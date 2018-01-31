from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP
import numpy as np


def add_flow(flows, num):
    key = 'flow'+str(num)
    value = 'flowlist'+str(num)
    value = []
    flows[key] = value
    return value


def sniff_packet(num):
    print("Start to sniff packets...")
    dpkt = sniff(filter="tcp and ip", count=num)
    print("Sniffing packets done")
    return dpkt


def output(flow):
    all = flow[5:]
    li = np.reshape(all, (-1, 5))
    return li


if __name__ == '__main__':
    dpkt = sniff_packet(30)
    num = 1
    test_images = []
    flows = {}
    add_flow(flows, num)
    flows['flow1'] = [dpkt[0][Ether].src, dpkt[0][Ether].dst, dpkt[0][Ether].sport, dpkt[0][Ether].dport, dpkt[0][Ether].proto]
    for packet in dpkt:
        IsGet = False
        srcIP = packet[Ether].src
        dstIP = packet[Ether].dst
        srcPort = packet[Ether].sport
        dstPort = packet[Ether].dport
        protocol = packet[Ether].proto
        timetolive = packet[IP].ttl
        window = packet[Ether].window
        length = packet[Ether].len
        print(srcIP, dstIP, srcPort, dstPort, protocol)
        for i in range(1, num+1):
            flow = flows['flow'+str(i)]
            print("i:"+str(i))
            IPs = (srcIP == flow[0] and dstIP == flow[1]) or (srcIP == flow[1] and dstIP == flow[0])
            Ports = (srcPort == flow[2] and dstPort == flow[3]) or (srcPort == flow[3] and dstPort == flow[2])
            Proto = (protocol == flow[4])
            if IPs and Ports and Proto:
                flow.append(srcPort, dstPort, timetolive, window, length)
                print("+1")
                print(flows)
                IsGet = True
                if len(flow) == 125:
                    test_images = output(flow)
                break
        if not IsGet:
            num = num + 1
            add_flow(flows, num)
            flows['flow'+str(num)] = [srcIP, dstIP, srcPort, dstPort, protocol, srcPort, dstPort, timetolive, window, length]
            print(flows)



