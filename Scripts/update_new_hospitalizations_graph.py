import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import os 
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
    hospitalized = list(state_data['hospitalizedCurrently'])[::-1]

    change_in_hospitalizations = []
    if len(hospitalized) > 2:
        change_in_hospitalizations = [hospitalized[i] - hospitalized[i-1] for i in range(1, len(hospitalized))]
    
    change_in_hospitalizations_moving_average = [np.mean(change_in_hospitalizations[x:x+7]) for x in range(len(change_in_hospitalizations) - 7)]

    dates = list(state_data['date'])[::-1]

    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), len(dates)//7 - 1):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Net Change in Hospitalizations")
    plt.title(f"COVID-19 Net Change Hospitalizations (7-Day Moving Avg) - {state}\nUsed covidtracking.com/api - Some data may be innacurate")
    plt.plot(change_in_hospitalizations_moving_average)
    plt.savefig(os.path.join("Graphs", f"NetChange{state}.png"))
    # plt.show()
    plt.cla()
# print(len(states))


