import numpy as np
rownum = 1
mylist = []
mylable = []
mynumlable = []


def z_ScoreNormalization(x, mu, sigma):
    x = (x - mu) / sigma
    return x


def strings_to_numbers(argument):
    switcher = {
        'BROWSING\n': 0,
        'MAIL\n': 1,
        'CHAT\n': 2,
        'AUDIO\n': 3,
        'VIDEO\n': 4,
        'FILE-TRANSFER\n': 5,
        'VOIP\n': 6,
        'P2P\n': 7
    }
    return switcher.get(argument, "nothing")


def MaxMinNormalization(x, Max, Min):
    if Max > Min:
        x = (x - Min) / (Max - Min)
    return x


w = open('Tor_10s_Layer2_10.csv', 'w')
wt = open('Tor_10s_Layer2_10_test.csv', 'w')
count = 0
with open('H:\dataset\TorPcaps\CSV\Scenario-B\TimeBasedFeatures-10s-Layer2.csv', 'r') as f:
    while rownum < 2:
        print(f.readline())
        rownum = rownum + 1
    for line in f.readlines():
        # if rownum < 10:
        raw = line.split(',')
        row = raw[5:]
        rownum = rownum + 1
        row[-1] = str(strings_to_numbers(row[-1]))
        mylist.append(row)
        # print(mylist)
    mydata = np.array(mylist, dtype=float)

    # print(mydata[:, 0])
    # print(len(mydata[:, 0]))
    # print(np.average(mydata[:, 0]))
    # print(np.std(mydata[:, 0]))

    for i in range(23):
        col = mydata[:, i]
        ave = np.average(col)
        std = np.std(col)
        maxnum = np.max(col)
        minnum = np.min(col)
        for x in range(len(col)):
            # col[x] = z_ScoreNormalization(col[x], ave, std)
            col[x] = MaxMinNormalization(col[x], maxnum, minnum)
    for row in mydata:
        count = count + 1
        if count % 10 == 0:
            for i in range(23):
                wt.write(str(row[i]))
                wt.write(',')
            wt.write(str(int(row[-1])))
            wt.write('\n')
        else:
            for i in range(23):
                w.write(str(row[i]))
                w.write(',')
            w.write(str(int(row[-1])))
            w.write('\n')

    # print(mydata)
    # np.savetxt("Tor_15s_Layer2_85.csv", mydata, fmt='%1.6f', delimiter=',')
    # np.savetxt("Tor_15s_Layer2_15_label.txt", mylable, fmt='%1.0e')
w.close()
wt.close()
