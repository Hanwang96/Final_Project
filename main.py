import numpy as np
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
from pandas import DataFrame

def create_MMR(KDA,time,win_perc):
    pass

def create_player():
    #ID, MMR, WaitingTime
    Size = 10000
    mu = 1120
    sigma = 425
    lower = 0
    upper = 3000
    # np.random.seed(0)
    X = truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    samples = X.rvs(Size)
    # plt.hist(samples, bins=50, normed=True, alpha=0.3, label='histogram')
    # plt.show()
    return samples

def create_waiting_time():
    # Uniform distribution
    Size = 10000
    lower = 0
    upper = 600
    # np.random.seed(0)
    s = np.random.uniform(lower, upper, Size)
    # plt.hist(s, 30, normed=True)
    # plt.show()
    return s

def create_dataframe(list, enter_time):
    dic = {'MMR': list, 'time': enter_time}
    player_frame = pd.DataFrame(dic)
    return player_frame

def create_match_pool(df, MMR_range):
    #find a time t1(interval)=5 to do the match
    #
    counter = 0
    interval = 5
    game_time = 60
    waitlist = df.sort_values(by = "time",ascending=True)
    match_list = []
    for i in range(0,240):
        counter += interval
        current_df = waitlist[waitlist["time"]<counter].sort_values(by = "MMR", ascending=True)
        # current_df = current_df

        for j in range(0,len(current_df)-1):
            if current_df.iloc[j,1]<=counter:
                for m in range(j+1,len(current_df)):
                    if current_df[m,1]<=counter:
                        if current_df.iloc[m,0] > current_df.iloc[j,0] - MMR_range and current_df.iloc[m,0] < current_df.iloc[j,0] + MMR_range:
                            match_list.append([current_df.iloc[j,0],current_df.iloc[m,0]])
                            current_df.iloc[j,1] += game_time
                            current_df.iloc[m,1] += game_time
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    continue

    return match_list

def compare_MMR(match_list, range):
    compare_list = []
    # Use some statistic ways to compute the comparison. Not just find the difference.
    for i in range(0,len(match_list)):
        if abs(match_list[i][0] - match_list[i][1]) > 0.7*range:
            compare_list.append(0)
        else:
            compare_list.append(1)
    return compare_list

def compute_win_lose(enemy_list):
    new_MMR = []
    # for j in range(0,len(match_list)):

    Ea = 1/(1+10**(enemy_list[0]-enemy_list[1]/400))
    Eb = 1 -Ea
    # Create random (1,100). If this number < Ea, A will win.
    number = 1
    if number < Ea:
        win_or_lose_A = 1
        win_or_lose_B = 0 #A win
    else:
        win_or_lose_A = 0
        win_or_lose_B = 1 #A lose
    # return win_or_lose
    new_MMR.append(enemy_list[0] + 16*(win_or_lose_A-Ea))
    new_MMR.append(enemy_list[1] + 16*(win_or_lose_B-Eb))
    return new_MMR



if __name__ == "__main__":
    list = create_player()
    time = create_waiting_time()
    df = create_dataframe(list,time)
    pool = create_match_pool(df,200)
    print(pool)