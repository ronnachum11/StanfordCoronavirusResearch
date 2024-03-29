import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import os 

r = requests.get("https://covidtracking.com/api/v1/states/daily.json")

# print(r.status_code)

with open('../data.json', 'w') as f:
    json.dump(r.json(), f)

data = pd.read_json("data.json")
states = set(data['state'])
states = sorted(states)
# print(data.columns)
for state in states:
    state_data = data.loc[data['state'] == state]
    hospitalized = list(state_data['hospitalizedCurrently'])[::-1]
    dates = list(state_data['date'])[::-1]

    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), len(dates)//7 - 1):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Total Current Hospitalizations")
    plt.title(f"COVID-19 Hospitalizations - {state}")
    plt.plot(hospitalized)
    plt.savefig(os.path.join("Graphs", f"Graph{state}.png"), bbox_inches='tight')
    # plt.show()
    plt.cla()
# print(len(states))


