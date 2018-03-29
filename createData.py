import os.path
from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP
import numpy as np


# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        if os.path.isfile(child):
            print(child)
            readFile(child)
            #             print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题
            continue
        eachFile(child)


# 遍历出结果 返回文件的名字
def readFile(filenames):
    a = filenames.split('/')
    type = a[1]
    file = a[2]
    dpkt = sniff(offline=filenames)

    # for packet in dpkt:
    #     srcPort = packet[Ether].sport
    #     dstPort = packet[Ether].dport
    #     timetolive = packet[IP].ttl
    #     length = packet[Ether].len
    #     protocol = packet[Ether].proto
    #     if protocol == 6:
    #         window = packet[Ether].window
    #     else:
    #         window = 0
    print(strings_to_numbers(type), file, len(dpkt))


def strings_to_numbers(argument):
    switcher = {
        'Audio-Streaming': 0,
        'Browsing': 1,
        'Chat': 2,
        'Email': 3,
        'File Transfer': 4,
        'P2P': 5,
        'Video-Streaming': 6,
        'VoIP': 7
    }
    return switcher.get(argument, "nothing")


def func(args,dire,fis): #回调函数的定义
    for f in fis:
        print(f)


# Audio-Streaming, Browsing, Chat, Email, File Transfer, P2P, Video-Streaming, VoIP
if __name__ == "__main__":
    # eachFile('H:\dataset\TorPcaps\\nonTor')
    eachFile('nonTor')
    # root = '/data/users/hebo/readpcap/nonTor'
    # os.path.walk(root, func, ())  # 遍历

