from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP


# 把pcap文件按时间间隔切割
def cut_pcap(filename, interval):  # 文件路径+文件名,流分段间隔
    dpkt = sniff(offline=filename)
    print(dpkt)
    start_time = dpkt[0].time
    end_time = start_time + interval
    packets = []  # 总时间内所有包
    time_packets = []  # 单位时间间隔内所有包
    for packet in dpkt:
        packet_time = packet.time
        if start_time <= packet_time <= end_time:
            time_packets.append(packet)
        elif packet_time > end_time:
            packets.append(time_packets)
            time_packets = []
            start_time = packet_time
            end_time = start_time + interval
            time_packets.append(packet)
    return packets


# 把pcap文件按时间间隔切割
def cut_packets(dpkt, interval):  # packetlist,流分段间隔
    print(dpkt)
    start_time = dpkt[0].time
    end_time = start_time + interval
    packets = []  # 总时间内所有包
    time_packets = []  # 单位时间间隔内所有包
    for packet in dpkt:
        packet_time = packet.time
        if start_time <= packet_time <= end_time:
            time_packets.append(packet)
        elif packet_time > end_time:
            packets.append(time_packets)
            time_packets = []
            start_time = packet_time
            end_time = start_time + interval
            time_packets.append(packet)
    return packets


def divide_flow(packets):
    flows = []  # 总时间内所有流
    time_flows = []  # 单位时间内所有流
    IPaddress = "10.152.152.11"
    for time_packets in packets:
        for packet in time_packets:
            ty = packet[Ether].type
            if ty == 0x800:  # IPV4格式，保证这个包是TCP或者UDP的
                protocol = packet[Ether].proto
                if protocol == 6 or protocol == 17:
                    srcIP = packet[IP].src
                    dstIP = packet[IP].dst
                    if srcIP == IPaddress or dstIP == IPaddress:
                        srcPort = packet[Ether].sport
                        dstPort = packet[Ether].dport
                        protocol = packet[Ether].proto
                        forTuple = [srcIP, dstIP, srcPort, dstPort, protocol]
                        backTuple = [dstIP, srcIP, dstPort, srcPort, protocol]
                        if forTuple in time_flows or backTuple in time_flows:
                            continue
                        else:
                            time_flows.append(forTuple)
        flows.append(time_flows)
        time_flows = []
    return flows


def get_feature(allflows, allpackets):
    IPaddress = "10.152.152.11"
    for time_flows in allflows:  # 每个时间区间内的所有流
        idx = allflows.index(time_flows)  # 对应的是第几个时间区间
        for flow in time_flows:
            forflow = []  # 存储这个流所有的前向包
            backflow = []  # 存储这个流所有的后向包
            twowayflow = []  # 存储这个流所有包
            fb_psec = 0  # 每秒的流字节数
            fp_psec = 0  # 每秒的流的包数
            for packet in allpackets[idx]:  # 遍历该区间内所有流量包，区分这个流的前向和后向流量
                ty = packet[Ether].type
                if ty == 0x800:  # IPV4格式，保证这个包是TCP或者UDP的
                    protocol = packet[Ether].proto
                    if protocol == 6 or protocol == 17:
                        srcIP = packet[IP].src
                        dstIP = packet[IP].dst
                        srcPort = packet[Ether].sport
                        dstPort = packet[Ether].dport
                        protocol = packet[Ether].proto
                        forTuple = [srcIP, dstIP, srcPort, dstPort, protocol]
                        backTuple = [dstIP, srcIP, dstPort, srcPort, protocol]
                        if forTuple == flow or backTuple == flow:
                            twowayflow.append(packet)
                            fb_psec = fb_psec + len(packet)
                            fp_psec = fp_psec + 1
                            if srcIP == IPaddress:
                                forflow.append(packet)
                            elif dstIP == IPaddress:
                                backflow.append(packet)
            start_time = twowayflow[0].time
            end_time = twowayflow[-1].time
            duration = end_time - start_time + 0.0001  # 流持续时间
            fb_psec = fb_psec / duration
            fp_psec = fp_psec / duration
        # 获取Forward Inter Arrival Time所有特征
            fiat = []
            if len(forflow) > 0:
                pre_for_time = forflow[0].time
                for for_packet in forflow[1:]:
                    for_time = for_packet.time
                    fiat.append(for_time - pre_for_time)
                fiat_mean = mymean(fiat)
                fiat_min = mymin(fiat)
                fiat_max = mymax(fiat)
                fiat_std = mystd(fiat)
            else:
                fiat_mean = 0
                fiat_min = 0
                fiat_max = 0
                fiat_std = 0
        # 获取Backward Inter Arrival Time所有特征
            biat = []
            if len(backflow) > 0:
                pre_back_time = backflow[0].time
                for back_packet in backflow[1:]:
                    back_time = back_packet.time
                    biat.append(back_time - pre_back_time)
                biat_mean = mymean(biat)
                biat_min = mymin(biat)
                biat_max = mymax(biat)
                biat_std = mystd(biat)
            else:
                biat_mean = 0
                biat_min = 0
                biat_max = 0
                biat_std = 0
        # 获取Flow Inter Arrival Time所有特征
            flowiat = []
            pre_flow_time = twowayflow[0].time
            for flow_packet in twowayflow[1:]:
                flow_time = flow_packet.time
                flowiat.append(flow_time - pre_flow_time)
            flowiat_mean = mymean(flowiat)
            flowiat_min = mymin(flowiat)
            flowiat_max = mymax(flowiat)
            flowiat_std = mystd(flowiat)
            feature = str(fiat_mean)+" "+str(fiat_min)+" "+str(fiat_max)+" "+str(fiat_std)+" "\
                      + str(biat_mean)+" "+str(biat_min)+" "+str(biat_max)+" "+str(biat_std)+" "\
                      + str(flowiat_mean)+" "+str(flowiat_min)+" "+str(flowiat_max)+" "+str(flowiat_std)+" "\
                      + str(fb_psec)+" "+str(fp_psec)+" "+str(duration)
            print(feature)


def mymin(mylist):
    if len(mylist) < 1:
        return 0
    else:
        return min(mylist)


def mymax(mylist):
    if len(mylist) < 1:
        return 0
    else:
        return max(mylist)


def mymean(mylist):
    if len(mylist) < 1:
        return 0
    else:
        return sum(mylist)/len(mylist)


def mystd(mylist):
    if len(mylist) < 1:
        return 0
    else:
        avg = mymean(mylist)
        sdsq = sum([(i - avg) ** 2 for i in mylist])
        stdev = (sdsq / (len(mylist))) ** .5
        return stdev


if __name__ == "__main__":
    file_name = "H:\dataset\TorPcaps\\nonTor\File_Transfer\SFTP_filetransfer.pcap"
    all_packets = cut_pcap(file_name, 5)
    all_flows = divide_flow(all_packets)
    get_feature(all_flows, all_packets)





