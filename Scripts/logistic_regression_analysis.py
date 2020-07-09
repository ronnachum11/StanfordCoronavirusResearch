import pandas as pd 
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import math
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
import scipy.optimize as optimize

path = "C:\\Users\\Ron\\StanfordCoronavirusResearch"

state = "GA"

## LINE TO CHANGE
if state == "FL":
    state_data = pd.read_csv(os.path.join(path, "RawData", "Florida", "fl_covid_track_api_data.csv"))
elif state == "AZ":
    state_data = pd.read_csv(os.path.join(path, "RawData", "Arizona", "az_covid_track_api_data.csv"))
elif state == "GA":
    state_data = pd.read_csv(os.path.join(path, "RawData", "Georgia", "ga_covid_track_api_data.csv"))

hospitalized = list(state_data['hospitalizedCumulative'])[::-1]
dates = list(state_data['date'])[::-1]

dates = [dates[i] for i in range(len(dates)) if not math.isnan(hospitalized[i])]
hospitalized = [i for i in hospitalized if not math.isnan(i)]

for i in range(1, len(hospitalized)):
    if math.isnan(hospitalized[i]):
        hospitalized[i] = hospitalized[i-1]

## LINES TO CHANGE
if state == "FL":
    names, reopening_dates = ["Phase 1", "Phase 2", "Current"], [20200504, 20200605, dates[-1]]
elif state == "AZ":
    names, reopening_dates = ["Phase 1", "Current"], [20200515, dates[-1]]
elif state == "GA":
    names, reopening_dates = ["Phase 1", "Current"], [20200424, dates[-1]]

lag_time = 12

reopening_indecies = [dates.index(i) for i in reopening_dates]
spike_expectations = [min(i + lag_time, len(hospitalized)) for i in reopening_indecies]

# regression_data = [[range(spike_expectations[i], spike_expectations[i+1]), hospitalized[spike_expectations[i]:spike_expectations[i+1]]] for i in range(len(spike_expectations) - 1)]
regression_data = [[range(i), hospitalized[:i]] for i in spike_expectations]
# print(regression_data)

x_values = range(int(len(hospitalized)*1.25))

def logistic(t, a, b, c):
    return c / (1 + a * np.exp(-b*t))

def exponential(t, a, b, c):
    return a * (b ** (c * t))

# regressions = {"Logistic": logistic, "Exponential": exponential}

colors, color_num = ['y', 'r', 'b'], 0
for i, data in enumerate(regression_data):
    x, y = data
    if i == len(regression_data) - 1:
        color_num = -1
    for regression_type in ['Logistic', 'Exponential']:
        p0 = np.random.exponential(size=3)
        if regression_type == "Logistic":
            bounds = (0, [100000., 100., 100000.])
            (a, b, c), cov = optimize.curve_fit(logistic, x, y, bounds=bounds, p0=p0)
            plt.plot(x_values, logistic(x_values, a, b, c), label=f'{names[i]} Trajectories', color=colors[color_num])
        else:
            if names[i] == "Current":
                bounds = (0, [5000., 1.1, 1000.])
                (a, b, c), cov = optimize.curve_fit(exponential, x, y, bounds=bounds, p0=p0)
                # plt.plot(x_values, exponential(x_values, a, b, c), color=colors[color_num])
    color_num += 1

x_ticks, x_tick_labels = [], []
for i in range(0, len(dates), len(dates)//7 - 1):
    date = str(dates[i])
    x_ticks.append(i)
    x_tick_labels.append(date[4:6] + "/" + date[6:8])
plt.xticks(x_ticks, x_tick_labels)
plt.xlabel("Dates")
plt.ylabel("Total Cumulative Hospitalizations")
plt.title(f"COVID-19 Hospitalizations - {state}\nUsed covidtracking.com/api - Some data may be innacurate")
plt.plot(hospitalized, label="Actual Data", color='k')

# plt.savefig(os.path.join("Graphs", "Cumulative Hospitalizations", f"{state}.png"))
plt.legend()
plt.show()