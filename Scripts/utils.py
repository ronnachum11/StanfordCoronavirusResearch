import numpy as np 

def moving_average(lst, cumulative=True, window=7):
    if len(lst) < window:
        return lst
    
    lst = lst[:window] + [np.mean(lst[i-window:i]) for i in range(window, len(lst))]

    if cumulative:
        lst = [lst[0]] + [max(lst[:i]) for i in range(1, len(lst))]

    return lst