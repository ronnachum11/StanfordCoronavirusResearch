import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import os 
import math
import time
import numpy as np
from ConvertCurrentToCumulative import hasCumulativeHospitalizations, getCumulativeHospitalizations

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

    index = 0
    for i in range(len(hospitalized)):
        if math.isnan(hospitalized[i]):
            index += 1
        else:
            break

    dates = dates[index:]
    hospitalized = hospitalized[index:]

    for i in range(1, len(hospitalized)):
        if math.isnan(hospitalized[i]):
            hospitalized[i] = hospitalized[i-1]

    calculated = False
    window = 21
    if len(hospitalized) < window:
        current_hospitalizations = list(state_data['hospitalizedCurrently'])[::-1]
        dates = list(state_data['date'])[::-1]

        dates = [dates[i] for i in range(len(dates)) if not math.isnan(current_hospitalizations[i])]
        current_hospitalizations = [i for i in current_hospitalizations if not math.isnan(i)]

        for i in range(1, len(current_hospitalizations)):
            if math.isnan(current_hospitalizations[i]):
                current_hospitalizations[i] = current_hospitalizations[i-1]

        if len(current_hospitalizations) > window:
            hospitalized = getCumulativeHospitalizations(current_hospitalizations, window)
            hospitalized = [0] * 7 + [np.mean(hospitalized[x - 7: x]) for x in range(7, len(hospitalized))]
            calculated = True

    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), max(1, len(dates)//7 - 1)):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Total Cumulative Hospitalizations")
    if not calculated:
        plt.title(f"COVID-19 Hospitalizations - {state}\nUsed covidtracking.com/api - Some data may be inaccurate")
    else:
        plt.title(f"COVID-19 Hospitalizations (Calculated) - {state}\nUsed covidtracking.com/api - Some data may be inaccurate")
    plt.plot(hospitalized)
    plt.savefig(os.path.join("Graphs", "General", "Cumulative Hospitalizations", f"{state}.png"))
    # plt.show()
    plt.cla()
# print(len(states))


