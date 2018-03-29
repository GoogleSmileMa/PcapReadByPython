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
        'Browsing\n': 0,
        'Email\n': 1,
        'Chat\n': 2,
        'Audio-Streaming\n': 3,
        'Video-Streaming\n': 4,
        'File_Transfer\n': 5,
        'VoIP\n': 6,
        'P2P\n': 7
    }
    return switcher.get(argument, "nothing")


def MaxMinNormalization(x, Max, Min):
    if Max > Min:
        x = (x - Min) / (Max - Min)
    return x


w = open('flow2_train.csv', 'w')
wt = open('flow2_test.csv', 'w')
count = 0
with open('flow2.csv', 'r') as f:
    # while rownum < 27:
    #     print(f.readline())
    #     rownum = rownum + 1
    for line in f.readlines():
        # if rownum < 10:
        # raw = line.split(',')
        # row = raw[5:]
        row = line.split(',')
        rownum = rownum + 1
        row[-1] = str(strings_to_numbers(row[-1]))
        mylist.append(row)
        # print(mylist)
    mydata = np.array(mylist, dtype=float)

    # print(mydata[:, 0])
    # print(len(mydata[:, 0]))
    # print(np.average(mydata[:, 0]))
    # print(np.std(mydata[:, 0]))

    for i in range(15):
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
            for i in range(15):
                wt.write(str(row[i]))
                wt.write(',')
            wt.write(str(int(row[-1])))
            wt.write('\n')
        else:
            for i in range(15):
                w.write(str(row[i]))
                w.write(',')
            w.write(str(int(row[-1])))
            w.write('\n')

    # print(mydata)
    # np.savetxt("Tor_15s_Layer2_85.csv", mydata, fmt='%1.6f', delimiter=',')
    # np.savetxt("Tor_15s_Layer2_15_label.txt", mylable, fmt='%1.0e')
w.close()
wt.close()
