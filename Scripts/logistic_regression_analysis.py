import pandas as pd 
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import math
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
import scipy.optimize as optimize

path = "C:\\Users\\Ron\\StanfordCoronavirusResearch"

states_dict = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

states_dict = {states_dict[name]: name for name in states_dict}

states = ["AZ", "FL", "GA", "OK", "SC"]

for state in states:
    state_data = pd.read_csv(os.path.join(path, "RawData", states_dict[state], f"{state.lower()}_covid_track_api_data.csv"))

    hospitalized = list(state_data['hospitalizedCumulative'])[::-1]
    dates = list(state_data['date'])[::-1]

    dates = [dates[i] for i in range(len(dates)) if not math.isnan(hospitalized[i])]
    hospitalized = [i for i in hospitalized if not math.isnan(i)]

    for i in range(1, len(hospitalized)):
        if math.isnan(hospitalized[i]):
            hospitalized[i] = hospitalized[i-1]

    ## LINES TO CHANGE
    if state == "FL":
        names, reopening_dates = ["Phase 1", "Phase 2"], [20200504, 20200605]
    elif state == "AZ":
        names, reopening_dates = ["Phase 1"], [20200515]
    elif state == "GA":
        names, reopening_dates = ["Phase 1"], [20200424]
    elif state == "OK":
        names, reopening_dates = ["Phase 1", "Phase 2", "Phase 3"], [20200501, 20200515, 20200601]
    elif state == "SC":
        names, reopening_dates = ["Phase 1", "Phase 2"], [20200504, 20200522]

    names.append("Current")
    reopening_dates.append(dates[-1])

    lag_time = 12

    reopening_indecies = [dates.index(i) for i in reopening_dates]
    spike_expectations = [min(i + lag_time, len(hospitalized)) for i in reopening_indecies]

    # regression_data = [[range(spike_expectations[i], spike_expectations[i+1]), hospitalized[spike_expectations[i]:spike_expectations[i+1]]] for i in range(len(spike_expectations) - 1)]
    regression_data = [[i, range(i), hospitalized[:i], range(i, int(len(hospitalized)*1.2))] for i in spike_expectations]
    # print(regression_data)

    def logistic(t, a, b, c):
        return c / (1 + a * np.exp(-b*t))

    def exponential(t, a, b, c):
        return a * (b ** (c * t))

    # regressions = {"Logistic": logistic, "Exponential": exponential}

    colors, color_num = ['r', 'y', 'g'], 0
    for i, data in enumerate(regression_data):
        index, x, y, x_values = data
        if i == len(regression_data) - 1:
            color_num = -1
        if names[i] != "Current":
            bounds = (0, [100000., 100., 100000.])

            while True:
                try:
                    p0 = np.random.exponential(size=3)
                    (a, b, c), cov = optimize.curve_fit(logistic, x, y, bounds=bounds, p0=p0)
                except Exception:
                    continue
                break
            y_values = logistic(x_values, a, b, c)
            y_values -= y_values[0] - hospitalized[index]

            plt.plot(x_values, y_values, linestyle='dashed', label=f'Pre-{names[i]} Trajectory', color=colors[color_num])
            plt.axvline(x=index - lag_time, color=colors[color_num])
        else:
            bounds = (0, [5000., 1.1, 1000.])

            while True:
                try:
                    p0 = np.random.exponential(size=3)
                    (a, b, c), cov = optimize.curve_fit(exponential, x, y, bounds=bounds, p0=p0)
                except Exception:
                    continue
                break
            y_values = exponential(x_values, a, b, c)
            y_values -= y_values[0] - hospitalized[-1]

            plt.plot(x_values, y_values, linestyle='dashed', label=f'{names[i]} Trajectory', color='b')
        color_num += 1

    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), len(dates)//7 - 1):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Total Cumulative Hospitalizations")
    plt.title(f"COVID-19 Hospitalizations - {state}")
    plt.plot(hospitalized, label="Actual Data", color='k')

    plt.legend()
    plt.savefig(os.path.join("Graphs", "Analysis", f"{state}.png"))
    plt.cla()
    # plt.show()