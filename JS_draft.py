import numpy as np
import collections
import pandas as pd
from numpy.linalg import cholesky
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import truncnorm
from scipy.stats import norm
from random import uniform
import threading as thd
import time
import datetime

def create_MMR(KDA,time,win_perc):
    pass

def create_player():
    #ID, MMR, WaitingTime
    Size = 1000
    mu = 1120
    sigma = 425
    lower = 0
    upper = 5000
    # np.random.seed(0)
    s  = np.random.normal(mu, sigma, Size)
    # plt.hist(s, 30, normed=True)
    # plt.show()

    return s

def create_entering_time():
    # Uniform distribution
    Size = 1000
    lower = 0
    upper = 600
    # np.random.seed(0)
    s = np.random.uniform(lower, upper, Size)
    # plt.hist(s, 30, normed=True)
    # plt.show()
    return s

# def create_match_pool(dic):
#     start = time.time()
#     # waiting_time_list = [0 for n in range(500)]
#     dic = sorted(dic.items(),key = lambda item : item[1])
#     print(dic)
#     match_list = []
#
#
#
#     end = time.time()
#     print (end - start)
#     return match_list

def compare_MMR(match_frame, rule, result):
    # Use some statistic ways to compute the comparison. Not just find the difference.
    diff = abs(match_frame.iloc[0,0] - match_frame.iloc[1,0])
    s = np.random.uniform(0,1)
    print(s)
    if diff > 0.7 * rule:
        if s < 0.2:
            if result:
                match_frame = match_frame.drop(index = 1, inplace = False)
            else:
                match_frame = match_frame.drop(index = 0, inplace = False)
    return match_frame

def compute_win_lose(match_frame):
    Ea = 1/(1+10**((match_frame.iloc[1,0]-match_frame.iloc[0,0])/400))
    print('e',Ea)
    Eb = 1-Ea
    # Create random (0,1). If this number < Ea, A will win.
    s = np.random.uniform(0, 1)
    print('s',s)
    if s < Ea:
        # A win
        win_or_lose = 1
        match_frame.iloc[0, 0] += 16 * (1 - Ea)
        match_frame.iloc[1, 0] += 16 * (0 - Eb)
    else:
        # A lose
        win_or_lose = 0
        match_frame.iloc[0, 0] += 16 * (0 - Ea)
        match_frame.iloc[1, 0] += 16 * (1 - Eb)
    return win_or_lose, match_frame

def compute_waiting_time():
    pass

def main_simulation(player):
    pass

if __name__ == "__main__":
    # list = create_player()
    # enter_time  = create_entering_time()
    # match_list = create_match_pool(player_dic)
    match_frame = pd.DataFrame([[2000, 60], [1500, 70]])
    result = compute_win_lose(match_frame)[0]
    print(result)
    print(compare_MMR(match_frame,200,result))


    # print(match_list)

