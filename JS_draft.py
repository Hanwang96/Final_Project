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
import pylab


def create_player():
    #ID, MMR, WaitingTime
    Size = 500
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

def create_entering_time():
    # Uniform distribution
    Size = 500
    lower = 0
    upper = 600
    # np.random.seed(0)
    s = np.random.uniform(lower, upper, Size)
    # plt.hist(s, 30, normed=True)
    # plt.show()
    return s

def create_dataframe(list, enter_time):
    dic = {'MMR': list, 'enter_time': enter_time}
    player_frame = pd.DataFrame(dic)
    #players' waiting time
    player_frame['wait_time'] = 0
    #the times a player end a matchmaking
    player_frame["times"] = 0
    #the status of players, online is 1. offline is 0
    player_frame['status'] = 1
    return player_frame



def match_begin(df):
    game_time = 60
    #generate result of a match
    result = compute_win_lose(df)[0]
    #determine if the player quits the game
    df_new = compare_MMR(df, 50, result)
    #generate new MMRs
    df_new = compute_win_lose(df_new)[1]
    # update the enter time
    df_new['enter_time'] += game_time
    #update the times of finishing a matchmaking
    df_new['times'] += 1
    return(df_new)


def waiting_for_too_long(df):
    #if player has been waiting for more than 60 seconds
    for index, row in df.iterrows():
        if row['wait_time']>60:
            # 20% probability players quit the game
            s = np.random.uniform(0,1)
            if s < 0.2:
                row['times'] += 1
                row['status'] = 0
    return df

def compare_MMR(match_frame, rule, result):
    # Use some statistic ways to compute the comparison. Not just find the difference.
    diff = abs(match_frame.iloc[0,0] - match_frame.iloc[1,0])
    s = np.random.uniform(0,1)
    print(s)
    if diff > 0.7 * rule:
        if s < 0.2:
            if result:
                match_frame.iloc[1,4] = 0
            else:
                match_frame.iloc[0,4] = 0
    return match_frame

def compute_win_lose(match_frame):
    Ea = 1/(1+10**((match_frame.iloc[1,0]-match_frame.iloc[0,0])/400))
    Eb = 1-Ea
    # Create random (0,1). If this number < Ea, A will win.
    s = np.random.uniform(0, 1)
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


def match_making(df, MMR_range):
    # find a time t1(interval)=5 to do the match
    interval = 5
    counter = interval
    current_df = pd.DataFrame()
    offline = pd.DataFrame()
    waitlist = df
    while counter < 1200:
        print('count',counter)
        waitlist = waitlist.sort_values(by="enter_time", ascending=True)
        # find players who would enter the matching pool before the given time point
        print('waitlist',waitlist)
        print('offline',offline)
        current_df = pd.concat([current_df,waitlist[waitlist["enter_time"] < counter]], ignore_index=True)
        if len(current_df) < 2:
            counter += interval
        else:
            current_df = current_df.sort_values(by="MMR", ascending=True)
            print('current_df', current_df)
            # record the waiting time
            current_df['wait_time'] += interval

            # delet players who enter the pool from wait list
            waitlist = waitlist[waitlist["enter_time"] >= counter]
            j = 0
            while True:
                flag = False
                if abs(current_df.iloc[j + 1, 0] - current_df.iloc[j, 0]) < MMR_range:
                    # match successfully
                    flag = True
                    match_player = current_df.iloc[j:j + 2]
                    after_match = match_begin(match_player)
                    print('after_match', after_match)
                    # players come back to wait list after they finish a match
                    waitlist = pd.concat([waitlist, after_match], ignore_index=True)
                    # mark players who enter a match
                    current_df.iloc[j:j + 2, 0] = None

                if flag:
                    j += 2
                else:
                    j += 1

                if j + 1 > len(current_df) - 2:
                    # finish traversal, delete players who finish a match from current df, keep players who didn't enter a match, waiting for next matchmaking
                    current_df = current_df.dropna(axis = 0, how = 'any')
                    # if the time players wait for matchmaking is too long
                    current_df = waiting_for_too_long(current_df)
                    break
            waitlist = pd.concat([waitlist,current_df[current_df['status'] == 0]], ignore_index=True)
            current_df = current_df.loc[df.loc[:, "status"] < 1, :]
            offline = pd.concat([offline, waitlist[waitlist['status'] == 0]],ignore_index=True)
            waitlist = waitlist[waitlist['status'] == 1]
            counter += interval

    waitlist = pd.concat([waitlist, offline], ignore_index=True)

    return waitlist

def MC_result_player(df):
    stays = df[df['status']>0]
    avg = df['MMR'].mean()
    std = df['MMR'].std()
    num_stays = len(stays)
    return num_stays,avg,std

def MC_result_MMR_avg(avg_list):
    x = np.linspace(0, 400, 20)
    y = avg_list
    plt.figure()
    plt.plot(x, y)

def MC_result_MMR_std(std_list):
    x = np.linspace(0, 400, 20)
    y = std_list
    plt.figure()
    plt.plot(x, y)

if __name__ == "__main__":
    list = create_player()
    enter_time  = create_entering_time()
    df = create_dataframe(list,enter_time)

    # for i in range(20,400,20):
    #     df_new = match_making(df,i)
    print( match_making(df,100))

    # print(match_list)

