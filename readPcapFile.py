from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP


def sniff_data(n, evenpcap, oddpcap):
    if n % 2 == 0:
        evenpcap = sniff(offline="Comnet/alldata_"+str(n)+".pcap")
        starttime1 = oddpcap[0].time * 1000000
        endtime1 = oddpcap[-1].time * 1000000
        starttime2 = evenpcap[0].time * 1000000
        endtime2 = evenpcap[-1].time * 1000000
    else:
        oddpcap = sniff(offline="Comnet/alldata_"+str(n)+".pcap")
        starttime1 = evenpcap[0].time * 1000000
        endtime1 = evenpcap[-1].time * 1000000
        starttime2 = oddpcap[0].time * 1000000
        endtime2 = oddpcap[-1].time * 1000000
    print(str(num) + ":" + str(starttime1) + "," + str(endtime1) + "," + str(starttime2) + "," + str(endtime2))


if __name__ == '__main__':
    evenpcap = sniff(offline="Comnet/alldata_0.pcap")
    oddpcap = sniff(offline="Comnet/alldata_1.pcap")
    starttime1 = evenpcap[0].time * 1000000
    endtime1 = evenpcap[-1].time * 1000000
    starttime2 = oddpcap[0].time * 1000000
    endtime2 = oddpcap[-1].time * 1000000
    evenfirst = True
    appname = 'rdp'
    print(str(1) + ":" + str(starttime1) + "," + str(endtime1) + "," + str(starttime2) + "," + str(endtime2))
    w = open(appname+'.txt', 'w')
    w.write(str(1) + ":" + str(starttime1) + "," + str(endtime1) + "," + str(starttime2) + "," + str(endtime2))
    count = 0
    lastcount = 0
    rowNum = 0
    packettime = 0
    num = 1
    allpackets = []
    with open('packets_default.info', 'r') as f:
        for line in f.readlines():
            if appname in line:
                rowNum = rowNum + 1
                flowstarttime = int(line.split('#')[1])
                flowendtime = int(line.split('#')[2])
                localport = int(line.split('#')[5])
                remoteport = int(line.split('#')[6])
                while flowstarttime > endtime1 and num < 643:  # 需要更新奇偶包内容
                    num = num + 1
                    evenfirst = (num % 2 != 0)
                    if evenfirst:  # 偶数pcap包在先
                        oddpcap = sniff(offline="Comnet/alldata_" + str(num) + ".pcap")
                        starttime1 = evenpcap[0].time * 1000000
                        endtime1 = evenpcap[-1].time * 1000000
                        starttime2 = oddpcap[0].time * 1000000
                        endtime2 = oddpcap[-1].time * 1000000
                    else:
                        evenpcap = sniff(offline="Comnet/alldata_" + str(num) + ".pcap")
                        starttime1 = oddpcap[0].time * 1000000
                        endtime1 = oddpcap[-1].time * 1000000
                        starttime2 = evenpcap[0].time * 1000000
                        endtime2 = evenpcap[-1].time * 1000000
                    print(str(num), str(starttime1), str(endtime1), str(starttime2), str(endtime2))
                    w.write(str(num)+':'+str(starttime1)+','+str(endtime1)+','+str(starttime2)+','+str(endtime2)+'\n')

                if evenfirst:
                    for packet in evenpcap:
                        packettime = packet.time*1000000
                        sport = packet[Ether].sport
                        dport = packet[Ether].dport
                        if flowstarttime <= packettime <= flowendtime and ((sport == localport and dport == remoteport) or (sport == remoteport and dport == localport)):
                            count = count + 1
                            allpackets.append(packet)
                            # w.write(str(count)+'\n')
                        elif packettime > flowendtime:
                            break
                    if packettime < flowendtime:
                        for packet in oddpcap:
                            packettime = packet.time * 1000000
                            sport = packet[Ether].sport
                            dport = packet[Ether].dport
                            if flowstarttime <= packettime <= flowendtime and ((sport == localport and dport == remoteport) or (sport == remoteport and dport == localport)):
                                count = count + 1
                                allpackets.append(packet)
                                # w.write(str(count)+'\n')
                            elif packettime > flowendtime:
                                break
                else:
                    for packet in oddpcap:
                        packettime = packet.time*1000000
                        sport = packet[Ether].sport
                        dport = packet[Ether].dport
                        if flowstarttime <= packettime <= flowendtime and ((sport == localport and dport == remoteport) or (sport == remoteport and dport == localport)):
                            count = count + 1
                            allpackets.append(packet)
                            # w.write(str(count)+'\n')
                        elif packettime > flowendtime:
                            break
                    if packettime < flowendtime:
                        for packet in evenpcap:
                            packettime = packet.time * 1000000
                            sport = packet[Ether].sport
                            dport = packet[Ether].dport
                            if flowstarttime <= packettime <= flowendtime and ((sport == localport and dport == remoteport) or (sport == remoteport and dport == localport)):
                                count = count + 1
                                allpackets.append(packet)
                                # w.write(str(count)+'\n')
                            elif packettime > flowendtime:
                                break
                print(rowNum, count, count-lastcount)
                w.write(str(rowNum)+' '+line.split('#')[0]+' '+str(count)+' '+str(count - lastcount)+'\n')
                lastcount = count
            else:
                continue
    wrpcap(appname, allpackets)
    w.close()


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
