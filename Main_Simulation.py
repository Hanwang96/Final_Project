import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compute():
    num_list = []
    avg_list = []
    std_list = []
    avg_list_inner = []
    std_list_inner = []
    num_list_inner = []

    for i in range(50, 300, 50):
        for j in range(1, 6):
            filename = "result_" + i + "_"+j+".csv"
            data = pd.read_csv(filename)
            stays = data[data['status'] > 0]
            avg = data['MMR'].mean()
            std = data['MMR'].std()
            num_stays = len(stays)

            num_list_inner.append(num_stays)
            avg_list_inner.append(avg)
            std_list_inner.append(std)

        avg = np.mean(avg_list_inner)
        avg_list.append(avg)
        std = np.mean(std_list_inner)
        std_list.append(std)
        num = np.mean(num_stays)
        num_list.append(num)
    return avg_list,std_list,num_list


def MC_result_MMR_avg(avg_list):
    x = np.linspace(50, 300, 50)
    y = avg_list
    plt.figure()
    plt.plot(x, y)

def MC_result_MMR_std(std_list):
    x = np.linspace(50, 300, 50)
    y = std_list
    plt.figure()
    plt.plot(x, y)

def MC_result_num(num_list):
    x = np.linspace(50, 300, 50)
    y = num_list
    plt.figure()
    plt.plot(x, y)

if __name__ == "__main__":
    filelist = compute()
    avglist = filelist[0]
    stdlist = filelist[1]
    numlist = filelist[2]
    MC_result_MMR_avg(avglist)
    MC_result_MMR_std(stdlist)
    MC_result_num(numlist)
