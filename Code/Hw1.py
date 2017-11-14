#Code for Hard EM
#!/usr/bin/env python
import csv
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
style.use('ggplot')
import os
import random
import math

def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    data = []
    for row in reader:
        data.append(" ".join(row))
    return data

def get_P(m, s, d, x):
    temp = math.exp((-1/2*s)*dist(x, m)**2)
    denom = (2*math.pi*s)**(d/2)
    return temp/denom

def sanitize(path):
    data_set = []
    with open(path, "rb") as f_obj:
        data = csv_reader(f_obj)

    for item in data:
        set = []
        for num in item.split(" "):
            set.append(float(num))
        data_set.append([set[0], set[1]])
    return data_set

def initialization(set):
    t1 = []
    t2 = []
    for item in set:
        rand =  random.randint(1, 2)
        if rand == 1:
            t1.append(item)
        else:
            t2.append(item)

    init_dict = {1:t1, 2:t2}

    return init_dict

def dist(x, y):
    return  math.sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2))

def assign(k1, k2, set):
    t1 = []
    t2 = []
    p_arr = []

    for item in set:
        # print dist(k1, item) < dist(k2, item)
        if (dist(k1, item) < dist(k2, item)):
            t1.append(item)
            p_arr.append([1, 0])
        else:
            t2.append(item)
            p_arr.append([0, 1])

    data_dict = {1: t1, 2: t2}
    return data_dict, p_arr


def find_mean(set):
    x = 0.0
    y = 0.0
    n = len(set)
    if (n == 0):
        return [0, 0]
    for item in set:
        x = x + item[0]
        y = y + item[1]

    return [x/n, y/n]

# def iter(k1, k2, data_dict):

def find_sigma(k, set):
    n = len(set)
    d = len(set[0])
    sum = 0
    for i in range(n):
        sum = sum + dist(k, set[i])

    return sum/(d*n)


def plot_set(set):
    arr = np.array(set)
    x, y = arr.T
    plt.scatter(x, y)
    plt.pause()

def plot_dict(data_dict, k1, k2, redraw):
    colors = list("rbrb")

    if redraw == True:
        plt.ion()
    else:
        plt.show()


    for item in data_dict.values():
        arr = np.asarray(item)
        (x, y) = arr.T
        plt.scatter(x, y, color=colors.pop())


    fig = plt.gcf()
    ax = fig.gca()
    c1 = plt.Circle((k1[0], k1[1]), find_sigma(k1, data_dict[1]), color=colors.pop(), fill=False, linewidth=2)
    c2 = plt.Circle((k2[0], k2[1]), find_sigma(k2, data_dict[2]), color=colors.pop(), fill=False, linewidth=2)
    ax.add_artist(c1)
    ax.add_artist(c2)


    if redraw == True:
        plt.pause(0.3)
        c1.remove()
        c2.remove()
    else:
        plt.ioff()
        plt.show()

def getRand():
    x = random.uniform(-5, 5)
    y = random.uniform(-5, 5)
    return [x, y]


def log_likelihood(set, m, s, p_arr, k):
    ll = 0.0
    n = len(set)
    for t in range(n):
        val = 0.0
        p = p_arr[t]
        for i in range(k):
            val = val + p[i]*get_P(m[i], s[i], 2, set[t])
        ll += np.log(val)
    return ll

def plot_LL(LL):
    plt.gcf().clear()
    plt.title("Log Likelihood")
    plt.plot(LL)
    plt.show()

if __name__ == '__main__':
    num = "1"
    # type = "small"
    type = "large"
    file_name =  "data_" + num + "_" + type + ".txt"
    file_path = os.getcwd() + "/data/" + file_name
    set = sanitize(file_path)
    # for item in set:
    #     print item
    # plot_set(set)
    k1 = getRand()
    k2 = getRand()
    data_dict = initialization(set)

    count = 0
    LL = []
    err = 0.1
    while(True):
        k1 = find_mean(data_dict[1])

        k2 = find_mean(data_dict[2])

        print ""

        temp_set = []
        for items in data_dict.values():
            for item in items:
                temp_set.append(item)
        temp_dict, p_arr = assign(k1, k2, temp_set)
        data_dict = temp_dict
        plot_dict(data_dict, k1, k2, True)

        ll = log_likelihood(set, [k1, k2], [find_sigma(k1, data_dict[1]), find_sigma(k2, data_dict[2])], p_arr, 2)
        LL.append(ll)
        print ll
        print ""

        if (count > 1):
            print abs(LL[count] - LL[count - 1])
            if (abs(LL[count] - LL[count - 1]) < err):
                break
        count = count + 1


    plot_dict(data_dict, k1, k2, False)
    plot_LL(LL)

    print "No of iterations for convergence " + str(count)