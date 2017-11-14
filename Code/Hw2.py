#Code for Soft Em
import csv
import random
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    data = []
    for row in reader:
        data.append(" ".join(row))
    return data


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

def getRand(k):
    x = random.uniform(-5+2*k, 5+2*k)
    y = random.uniform(-5+2*k, 5+2*k)
    return [x, y]

def dist(x, y):
    return np.linalg.norm(np.asarray(x) - np.asarray(y))


def get_P(m, s, d, x):
    temp = math.exp((-1/2*s)*dist(x, m)**2)
    denom = (2*math.pi*s)**(d/2)
    return temp/denom

def get_sum(m, s, p, x):
    n = len(p)
    sum = 0;
    for i in range(n):
        sum = sum + p[i]*get_P(m[i], s[i], 2, x)

    return sum

def assign(set, p_arr):
    t1 = []
    t2 = []

    for i in range(len(set)):
        item = set[i]
        if (p_arr[i][0] > p_arr[i][1]):
            t1.append(item)
        else:
            t2.append(item)

    data_dict = {0: t1, 1: t2}
    return data_dict

def find_mean(set, p_arr, type):
    x = 0.0
    y = 0.0
    n = len(set)
    if (n == 0):
        return [0, 0]
    for i in range(n):
        x = x + p_arr[i][type] * set[i][0]
        y = y + p_arr[i][type] * set[i][1]

    return [x/n, y/n]

def find_sigma(m, set, p_arr, type):
    n = len(set)
    if n == 0:
        return 0
    d = len(set[0])
    sum = 0
    for i in range(n):
        sum = sum + p_arr[i][type] * dist(m, set[i])

    return sum/(d*n)


def e_step(m, s, p_arr, set):
    p_arr_new = []
    if len(set) == 0:
        return p_arr_new
    for i in range(len(set)):
        x = set[i]
        p = p_arr[i]
        p0 = p[0] * get_P(m[0], s[0], 2, x) / get_sum(m, s, p, x)
        p1 = p[1] * get_P(m[1], s[1], 2, x) / get_sum(m, s, p, x)
        p_arr_new.append([p0, p1])
    return p_arr_new

def plot_dict(data_dict, m, s, redraw, heading=""):
    colors = list("rbrb")
    k1 = m[0]
    k2 = m[1]
    if redraw == True:
        plt.ion()
    else:
        plt.show()


    for item in data_dict.values():
        if (len(item) > 0):
            arr = np.asarray(item)
            (x, y) = arr.T
            plt.scatter(x, y, color=colors.pop())


    fig = plt.gcf()
    ax = fig.gca()
    c1 = plt.Circle((k1[0], k1[1]), s[0], color=colors.pop(), fill=False, linewidth=2)
    c2 = plt.Circle((k2[0], k2[1]), s[1], color=colors.pop(), fill=False, linewidth=2)
    ax.add_artist(c1)
    ax.add_artist(c2)


    if redraw == True:
        plt.pause(0.3)
        c1.remove()
        c2.remove()
    else:
        plt.title(heading)
        plt.ioff()
        plt.show()

def m_step(set, p_arr):
    m = []
    s = []

    for type in [0, 1]:
        mean = find_mean(set, p_arr, type)
        sigma = find_sigma(mean, set, p_arr, type)
        m.append(mean)
        s.append(sigma)

    return m, s

def get_rand_p_arr(set):
    n = len(set)
    p_arr = []
    for i in range(n):
        p = random.uniform(0, 1)
        p_arr.append([p, 1 - p])

    return p_arr

def plot_true(set, title = ""):
    n = len(set)
    t0 = []
    t1 = []
    for i in range(n):
        if(i > n/2):
            t0.append(set[i])
        else:
            t1.append(set[i])
    data_dict = {0: t0, 1: t1}
    plot_dict(data_dict, [[0, 0], [0, 0]], [0, 0], False, title)
    return 0





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
    k = 2
    num = "2"
    # type = "small"
    type = "large"
    file_name = "data_" + num + "_" + type + ".txt"
    file_path = os.getcwd() + "/data/" + file_name
    set = sanitize(file_path)

    m = []
    s = []
    LL = []
    for i in range(k):
        m.append(getRand(k))
        s.append(random.uniform(0, 5))
    # p = [0.5, 0.5]
    err = 0.005

    p_arr = get_rand_p_arr(set)
    data_dict = assign(set, p_arr)

    plot_dict(data_dict, m, s, True)

    count = 0
    data_split = []
    while True:
        m, s = m_step(set, p_arr)
        p_arr_new = e_step(m, s, p_arr, set)

        p_arr = p_arr_new

        data_dict = assign(set, p_arr)

        plot_dict(data_dict, m, s, True)
        ll = log_likelihood(set, m, s, p_arr, k)
        LL.append(ll)
        print ll
        print ""

        if (count > 1):
            print abs(LL[count] - LL[count - 1])
            if (abs(LL[count] - LL[count - 1]) < err):
                break
        count = count + 1

    plot_dict(data_dict, m, s, False, "Final Prediction")
    plot_true(set, "True Distribution")
    plot_LL(LL)



