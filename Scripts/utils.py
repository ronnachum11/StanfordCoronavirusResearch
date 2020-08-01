import numpy as np 

def moving_average(lst, window=7):
    if len(lst) < window:
        return lst
    
    return lst[:window] + [np.mean(lst[i-window:i]) for i in range(window, len(lst))]