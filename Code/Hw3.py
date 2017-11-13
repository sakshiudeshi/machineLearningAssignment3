#Code for Soft Em with variable k
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

def getRand():
    x = random.uniform(-5, 5)
    y = random.uniform(-5, 5)
    return [x, y]

def dist(x, y):
    return np.linalg.norm(np.asarray(x) - np.asarray(y))

# def dist(x, y):
#     return  math.sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2))

def get_P(m, s, d, x):
    temp = math.exp((-1/2*s)*dist(x, m)**2)
    denom = (2*math.pi*s)**(d/2)
    # print s
    return temp/denom

def get_sum(m, s, p, x):
    n = len(p)
    sum = 0;
    for i in range(n):
        sum = sum + p[i]*get_P(m[i], s[i], 2, x)

    return sum

def find_max_p(p, k):
    max = 0
    # print p
    for i in range(k):
        if (p[i] > p[max]):
            max = i
    return max

def assign(set, p_arr, k):
    t = []
    for i in range(k):
        t.append([])


    for i in range(len(set)):
        item = set[i]
        # print "p arr " + str(p_arr[i][0] > p_arr[i][1])
        max = find_max_p(p_arr[i], k)
        t[max].append(item)

    data_dict = {}
    for i in range(k):
        data_dict[i] = t[i]
    return data_dict

def find_mean(set, p_arr, type):
    x = 0.0
    y = 0.0
    n = len(set)
    for i in range(n):
        x = x + p_arr[i][type] * set[i][0]
        y = y + p_arr[i][type] * set[i][1]

    return [x/n, y/n]

def find_sigma(m, set, p_arr, type):
    # print set
    n = len(set)
    if n == 0:
        return 0
    d = len(set[0])
    sum = 0
    for i in range(n):
        sum = sum + p_arr[i][type] * dist(m, set[i])

    return sum/(d*n)


def e_step(m, s, p_arr, set, k):
    p_arr_new = []
    if len(set) == 0:
        return p_arr_new
    for i in range(len(set)):
        x = set[i]
        p = p_arr[i]
        temp = []
        for i in range(k):
            p0 = p[i] * get_P(m[i], s[i], 2, x) / get_sum(m, s, p, x)
            temp.append(p0)
        p_arr_new.append(temp)
    return p_arr_new

def plot_dict(data_dict, m, s, redraw, k, heading=""):
    colors_scat = list("rbgcmyk")
    colors_circ = list("rbgcmyk")

    if redraw == True:
        plt.ion()
    else:
        plt.show()


    for item in data_dict.values():
        if (len(item) > 0):
            arr = np.asarray(item)
            (x, y) = arr.T
            plt.scatter(x, y, color=colors_scat.pop())


    fig = plt.gcf()
    ax = fig.gca()
    c = []
    for i in range(k):
        c.append(plt.Circle((m[i][0], m[i][1]), s[i], fill=False, color=colors_circ.pop()))

    # print c
    for j in range(k):
        ax.add_artist(c[j])


    if redraw == True:
        plt.pause(0.3)
        for i in range(k):
            c[i].remove()
    else:
        plt.title(heading)
        plt.ioff()
        plt.show()

def m_step(set, p_arr, k):
    m = []
    s = []
    # for type in [0, 1]:
    #     set = data_dict[type]
    #     mean = find_mean(set, p_arr, type)
    #     sigma = find_sigma(mean, set, p_arr, type)
    #     m.append(mean)
    #     s.append(sigma)

    for i in range(k):
        mean = find_mean(set, p_arr, i)
        sigma = find_sigma(mean, set, p_arr, i)
        m.append(mean)
        s.append(sigma)

    return m, s

def get_rand_p_arr(set, k):
    n = len(set)
    p_arr = []
    for i in range(n):
        temp = np.random.dirichlet(np.ones(k), size=1)
        list = temp.tolist()
        for item in list:
            p_arr.append(item)
    return p_arr



    return p_arr



# def get_P(m, s, d, x):



if __name__ == '__main__':
    k = 2
    num = "2"
    # type = "small"
    type = "large"

    file_name = "data_" + num + "_" + type + ".txt"
    # file_name = "mystery_" + num + ".txt"
    file_path = os.getcwd() + "/data/" + file_name
    set = sanitize(file_path)

    m = []
    s = []
    for i in range(k):
        m.append(getRand())
        s.append(random.uniform(0, 5))
    # p = [0.5, 0.5]

    p_arr = get_rand_p_arr(set, k)
    # print p_arr
    data_dict = assign(set, p_arr, k)

    plot_dict(data_dict, m, s, True, k)
    # print p_arr
    # m, s = m_step(set, p_arr)
    # p_arr = e_step(m, s, p_arr, set)
    # print "m is " + str(m)
    # print "s is " + str(s)
    # print len(data_dict[1])
    count = 0
    data_split = []
    while True:
        m, s = m_step(set, p_arr, k)
        # print "m is " + str(m)
        # print "s is " + str(s)
        p_arr_new = e_step(m, s, p_arr, set, k)

        p_arr = p_arr_new

        # print p_arr

        data_dict = assign(set, p_arr, k)
        # ll.append(log_likelihood(set, m, s))
        # print ""
        temp = []
        for i in range(k):
            temp.append(len(data_dict[i]))
        data_split.append(temp)
            # print len(data_dict[i])
        # print ""
        plot_dict(data_dict, m, s, True, k)
        if(count > 100):
            if (data_split[count] == data_split[count - 1]):
                break

        count = count + 1


    print data_split

    plot_dict(data_dict, m, s, False, k, "Final Prediction")



