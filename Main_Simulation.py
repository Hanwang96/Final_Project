import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compute():
    list = [5,10,20,30,40,50,75,100,250,400]
    num0_list = []
    num1_list = []
    num2_list = []
    avg_list = []
    std_list = []
    avg_list_inner = []
    std_list_inner = []
    num0_list_inner = []
    num1_list_inner = []
    num2_list_inner = []
    for i in list:
        for j in range(1,4):
            i = str(i)
            j = str(j)
            filename = "result" + i + "_"+j+".csv"
            data = pd.read_csv(filename)
            stays2 = data[data['status'] > 1]
            stays0 = data[data['status'] < 1]

            avg = data['MMR'].mean()
            std = data['MMR'].std()
            num_stays0 = len(stays0)

            num_stays2 = len(stays2)
            num_stays1 = len(data) - len(stays2) - len(stays0)
            num0_list_inner.append(num_stays0)
            num1_list_inner.append(num_stays1)
            num2_list_inner.append(num_stays2)
            avg_list_inner.append(avg)
            std_list_inner.append(std)

        avg = np.mean(avg_list_inner)
        avg_list.append(avg)
        std = np.mean(std_list_inner)
        std_list.append(std)
        num0 = np.mean(num0_list_inner)
        num1 = np.mean(num1_list_inner)
        num2 = np.mean(num2_list_inner)

        num0_list.append(num0)
        num1_list.append(num1)
        num2_list.append(num2)
    return avg_list,std_list,num0_list,num1_list,num2_list


def MC_result_MMR_avg(avg_list):
    list = [5, 10, 20, 30, 40, 50, 75, 100, 250, 400]
    x = list
    y = avg_list
    plt.figure()
    plt.xlabel('Range of MMR')
    plt.ylabel('Average MMR of Players')
    plt.title('The change of mu in MMR distribution')
    plt.plot(x, y)
    plt.show()


def MC_result_MMR_std(std_list):
    list = [5, 10, 20, 30, 40, 50, 75, 100, 250, 400]
    x = list
    y = std_list
    plt.figure()
    plt.plot(x, y)
    plt.xlabel('Range of MMR')
    plt.ylabel('The standard deviation MMR')
    plt.title('The change of sigma in MMR distribution')
    plt.show()


def MC_result_num(num_list,i):
    list = [5, 10, 20, 30, 40, 50, 75, 100, 250, 400]
    x = list
    y = num_list
    plt.figure()
    plt.xlabel('Range of MMR')
    plt.ylabel('Number of players')

    if i == 0:
        plt.title('Number of players who quittd because waiting time')
    elif i ==1:
        plt.title('Number of players who quittd because bad experience')
    elif i ==2:
        plt.title('Number of players who still online')

    plt.plot(x, y)
    plt.show()

if __name__ == "__main__":

    filelist = compute()
    avglist = filelist[0]
    stdlist = filelist[1]
    num0list = filelist[2]
    num1list = filelist[3]
    num2list = filelist[4]

    MC_result_MMR_avg(avglist)
    MC_result_MMR_std(stdlist)
    MC_result_num(num0list,0)
    MC_result_num(num1list,1)
    MC_result_num(num2list,2)

    print(num0list)
    print(avglist)
    print(stdlist)