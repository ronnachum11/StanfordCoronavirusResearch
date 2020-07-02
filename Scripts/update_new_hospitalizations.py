import requests
import pandas as pd
import json
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os
import time
import numpy as np

r = requests.get("https://covidtracking.com/api/v1/states/daily.json")

# print(r.status_code)

with open('data.json', 'w') as f:
    json.dump(r.json(), f)

data = pd.read_json("data.json")
states = set(data['state'])
states = sorted(states)
# print(data.columns)
for state in states:
    state_data = data.loc[data['state'] == state]
    hospitalized = list(state_data['hospitalizedCumulative'])[::-1]
    dates = list(state_data['date'])[::-1]

    hospitalized = [v for v in hospitalized if not math.isnan(v)]
    dates = dates[len(dates) - len(hospitalized):]

    new_hospitalizations = []
    if len(hospitalized) > 2:
        new_hospitalizations = [hospitalized[i] - hospitalized[i-1] for i in range(1, len(hospitalized))]
    
    initial_moving_average = [np.mean(new_hospitalizations[:i]) if len(new_hospitalizations[:i]) > 0 else 0 for i in range(7)]
    new_hospitalizations_moving_average =  initial_moving_average + [np.mean(new_hospitalizations[x-7:x]) for x in range(7, len(new_hospitalizations))]

    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), max(len(dates)//7 - 1, 1)):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])

    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Net Change in Hospitalizations")
    
    plt.title(f"COVID-19 New Hospitalizations - {state}\nUsed covidtracking.com/api - Some data may be innacurate")
    plt.bar(range(len(new_hospitalizations)), new_hospitalizations)
    plt.plot(new_hospitalizations_moving_average, color='k', label='7 Day Moving Average')
    plt.plot([0 for i in range(len(new_hospitalizations_moving_average))], color='r', label='Zero')
    plt.legend()

    plt.savefig(os.path.join("Graphs", f"NewHospitalizations{state}.png"))
    # plt.show()
    plt.cla()

