import numpy as np
import pandas as pd
from scipy.stats import truncnorm
import time

def create_player(Size):
    """
    We suppose that in an online game, the level distribution of players follows a normal distribution. We generate players' MMRs based on the (1125,425) normal distribution.
    :param Size: the number of players in the simulation
    :return: players' MMRs as a list
    >>> A = create_player(1000)
    >>> len(A)
    1000
    """
    mu = 1120
    sigma = 425
    lower = 0
    upper = 3000
    X = truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    samples = X.rvs(Size)

    return samples

def create_entering_time(Size):
    """
    We suppose that all the players will login and join the match pool within 10 minutes which follows a uniform distribution. Thus, a uniform distribution U[0,600] is used to represented the second that a player join the match pool.
    :param Size: the number of players in the simulation
    :return: time points of entering game matchmaking of all players as a list
    >>> A = create_entering_time(1000)
    >>> len(A)
    1000
    """
    # Uniform distribution
    lower = 0
    upper = 600
    s = np.random.uniform(lower, upper, Size)
    return s

def create_dataframe(list, enter_time):
    """
    Generating a dataframe containing every player"s MMR, entering time point, waiting time in the entire simulation, times of quiting a matchmaking, status of online or offline and wait time of each matchmaking.
    :param list: players' MMRs as a list
    :param enter_time: time points of entering game matchmaking of all players as a list
    :return: a dataframe with column MMR, enter_time, wait_time, times, status, every_wait_time
    >>> list = [0,1]
    >>> enter_time = [1,0]
    >>> create_dataframe(list,entertime)
        MMR  enter_time  wait_time  times  status  every_wait_time
    0    0   1          0      0       2                0
    1    1   0          0      0       2                0
    """
    dic = {'MMR': list, 'enter_time': enter_time}
    player_frame = pd.DataFrame(dic)
    # players'waiting time in overall simulation
    player_frame['wait_time'] = 0
    # the times a player end a matchmaking
    player_frame["times"] = 0
    # the status of players, online is 1. offline is 0
    player_frame['status'] = 2
    # player's waiting time in every matchmaking
    player_frame['every_wait_time'] = 0
    return player_frame



def match_begin(df):
    """
     The time of a match is set as 60 seconds. After a match, the MMR of two players will be updated based on the result (use another function to determine the result).
    :param df: a dataframe with column MMR, enter_time, wait_time, times, status, every_wait_time
    :return: a dataframe with undated column MMR, enter_time, wait_time, times, status, every_wait_time
    >>> A = np.array([1,0,0,0,0,0,0,0,0,0,0,0]).reshape(2,6)
    >>> B = pd.DataFrame(A)
    >>> match_begin(B) #doctest: +ELLIPSIS
    """
    game_time = 60
    # generate result of a match
    result = compute_win_lose(df)[0]
    # determine if the player quits the game
    df_new = compare_MMR(df, result,0.3)
    # generate new MMRs
    df_new = compute_win_lose(df_new)[1]
    # update the enter time
    df_new.iloc[:,1] += game_time
    # update the times of finishing a matchmaking
    df_new.iloc[:,3] += 1
    return(df_new)


def waiting_for_too_long(df,p1,p2):
    """
    Players whose average waiting time are higher than 30 seconds will quit the game at 30% after each matchmaking.
    Players whose average waiting time are higher than 60 seconds will quit the game at 60% after each matchmaking.
    :param df:a dataframe with column MMR, enter_time, wait_time, times, status, every_wait_time
    :return:a dataframe with updated status column
    >>> A = np.array([1,0,0,0,2,40,0,0,0,0,2,70]).reshape(2,6)
    >>> B = pd.DataFrame(A)
    >>> waiting_for_too_long(B,1,0).iloc[0,4]
    0
    >>> waiting_for_too_long(B,1,0).iloc[0,3]
    1
    >>> waiting_for_too_long(B,1,0).iloc[1,4]
    2
    """

    for i in range(len(df)):

        s = np.random.uniform(0, 1)
        # if player has been waiting for more than 30 seconds
        # there is a probability players quit the game
        if df.iat[i,5]>30 and df.iat[i,5] <61:
            if s < p1:
                df.iat[i,3] += 1
                df.iat[i,4] = 0
        # if player has been waiting for more than 60 seconds
        # there is a probability players quit the game
        elif df.iat[i,5]>60:
            if s <p2:
                df.iat[i, 3] += 1
                df.iat[i, 4] = 0
    return df

def compare_MMR(match_frame, result, p):
    '''
    compare players' MMRs and if the difference is too high, the loser's playing experience would be terrible and he or she will probably quit the game.
    :param match_frame:a dataframe with column MMR, enter_time, wait_time, times, status, every_wait_time
    :param result: the result of the match as boolean variable (0 or 1)
    :return: a dataframe with updated status
    >>> A = np.array([1200,0,0,0,2,0,100,0,0,0,2,0]).reshape(2,6)
    >>> B = pd.DataFrame(A)
    >>> compare_MMR(B,1,1).iloc[1,4]
    1
    >>> compare_MMR(B,0,1).iloc[0,4]
    1
    '''
    # Use statistic way to compute the comparison.
    diff = match_frame.iat[0,0] - match_frame.iat[1,0]
    if diff < 0:
        base = match_frame.iat[1,0]
    else:
        base = match_frame.iat[0,0]
    s = np.random.uniform(0,1)
    # if the difference is too huge, update players' status
    if abs(diff)/base > 0.1:
        if s < p:
            if result:
                match_frame.iat[1,4] = 1
            else:
                match_frame.iat[0,4] = 1
    return match_frame

def compute_win_lose(match_frame):
    """
    dtermine the result of a match based on players' MMRs by elo rating system
    :param match_frame: :a dataframe with column MMR, enter_time, wait_time, times, status, every_wait_time
    :return: a data frame with updated column MMR
    >>> A = np.array([1500,0,0,0,2,0,0,0,0,0,2,0]).reshape(2,6)
    >>> B = pd.DataFrame(A)
    >>> compute_win_lose(B)[0]
    1
    """
    Ea = 1/(1+10**((match_frame.iat[1 ,0]-match_frame.iat[0,0])/400))
    Eb = 1-Ea
    # Create random (0,1). If this number < Ea, A will win.
    s = np.random.uniform(0, 1)
    if s < Ea:
        # A win
        win_or_lose = 1
        match_frame.iat[0, 0] += 16 * (1 - Ea)
        match_frame.iat[1, 0] += 16 * (0 - Eb)
    else:
        # A lose
        win_or_lose = 0
        match_frame.iat[0, 0] += 16 * (0 - Ea)
        match_frame.iat[1, 0] += 16 * (1 - Eb)
    if match_frame.iat[0, 0] < 0:
        match_frame.iat[0, 0] = 0
    if match_frame.iat[1, 0] < 0:
        match_frame.iat[1, 0] = 0
    return win_or_lose, match_frame


def match_making(df, MMR_range,time_limit):
    '''
    simulation of matchmaking. Use a counter to count the time has passed and let the players whose enter time are lower than counter enter the match pool. Then create a small dataframe and sort it by MMR. We make the match every 5 seconds. If the first player can't be the opponent of the next player, the first player would be left and moved to next time of matchmaking.
    :param df: a dataframe with column MMR, enter_time, wait_time, times, status, every_wait_time
    :param MMR_range: the rule we use to test as an integer
    :param time_limit: time the simulation lasts as an integer
    :return: a dataframe with updated column
    >>> A = np.array([1500,0,0,0,2,0,1600,0,0,0,2,0]).reshape(2,6)
    >>> B = pd.DataFrame(A)
    >>> C = match_making(B,200,60)
    >>> len(C)
    2
    '''
    # find a time t1(interval)=5 to do the match
    interval = 5
    counter = interval
    current_df = pd.DataFrame()
    offline = pd.DataFrame()
    waitlist = df

    while counter < time_limit:
        waitlist = waitlist.sort_values(by="enter_time", ascending=True)
        # find players who would enter the matching pool before the given time point
        current_df = pd.concat([current_df,waitlist[waitlist["enter_time"] < counter]], ignore_index=True)
        if len(current_df) < 2:
            counter += interval
        else:
            current_df = current_df.sort_values(by="MMR", ascending=True)
            # record the waiting time
            current_df['wait_time'] += interval
            current_df['every_wait_time'] += interval
            # delet players who enter the pool from wait list
            waitlist = waitlist[waitlist["enter_time"] >= counter]
            j = 0
            while True:
                flag = False
                if abs(current_df.iat[j + 1, 0] - current_df.iat[j, 0]) < MMR_range:
                    # match successfully
                    flag = True
                    match_player = current_df.iloc[j:j + 2].copy()
                    after_match = match_begin(match_player)
                    after_match.iloc[:,5] = 0
                    # players come back to wait list after they finish a match
                    waitlist = pd.concat([waitlist, after_match], ignore_index=True)
                    # mark players who enter a match
                    current_df.iloc[j:j + 2, 0] = None
                if flag:
                    # if the pair of players match successfully, look for next pair
                    j += 2
                    # if the pair of players didn't match successfully, see if the latter player could match with the next player
                else:
                    j += 1

                if j + 1 > len(current_df) - 2:
                    # finish traversal, delete players who finish a match from current df, keep players who didn't enter a match, waiting for next matchmaking
                    current_df = current_df.dropna(axis = 0, how = 'any')
                    # if the time players wait for matchmaking is too long
                    current_df = waiting_for_too_long(current_df,0.4,0.8)
                    break
            # move the players who are offline from current_df to waitlist
            waitlist = pd.concat([waitlist,current_df[current_df['status'] < 2]], ignore_index=True)
            current_df = current_df.loc[current_df.loc[:, "status"] > 1, :]
            # move the players who are offline from waitlist to offline
            offline = pd.concat([offline, waitlist[waitlist['status'] <2]],ignore_index=True)
            waitlist = waitlist[waitlist['status'] == 2]
            counter += interval
    # integrate the dataframe
    waitlist = pd.concat([waitlist, offline, current_df], ignore_index=True)

    return waitlist

def save_site(df):
    """
    write the result we get as a csv file
    :param df: a dataframe with column MMR, enter_time, wait_time, times, status, every_wait_time
    :return: none
    """
    df.to_csv(path_or_buf='result.csv',index = False)

if __name__ == "__main__":
    # number of players is 1000
    Size = 1000
    # time limination is 3000 seconds
    time_limit = 3000
    time1 = time.time()
    # generate the MMRs
    list = create_player(Size)
    #g enerate the enter time
    enter_time  = create_entering_time(Size)
    # create the data frame containing all information
    df = create_dataframe(list,enter_time)
    # get a new data frame after simulation
    MMR_range = input('Please input the MMR_range you want to test:')
    df_new = match_making(df,int(MMR_range),time_limit)
    # save the dataframe as a csv file
    save_site(df_new)
    time2 = time.time()



