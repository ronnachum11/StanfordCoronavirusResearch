import pandas as pd
import os
import math
import matplotlib.pyplot as plt
import numpy as np 

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
path = "C:\\Users\\Ron\\StanfordCoronavirusResearch"

def doubling_time(m, y, window):
    y1, y2 = y[m - window], y[m]

    if y1 == 0:
        return 0

    return (window) * np.log(2) / np.log(y2 / y1)

for state in ["Florida"]: # states_dict:
    state_data = pd.read_csv(os.path.join(path, "RawData", state, f"{states_dict[state].lower()}_covid_track_api_data.csv"))

    hospitalized = list(state_data['hospitalizedCumulative'])[::-1]
    dates = list(state_data['date'])[::-1]

    num, count = hospitalized[0], 0
    while math.isnan(num):
        if count >= len(hospitalized):
            break
        num = hospitalized[count]
        count += 1
    hospitalized, dates = hospitalized[count:], dates[count:]
    
    if state == "Florida":
        names, reopening_dates = ["Phase 1", "Phase 2"], [20200504, 20200605]
        lag_times = [7, 14]

        colors = ['r', 'y', 'g']

        new_names = [[f"{name} Reopening"] + [f"{name} Reopening + {lag_time} Days" for lag_time in lag_times] for name in names]
        reopening_indecies = [dates.index(i) for i in reopening_dates]
        # print(dates)
        spike_expectations = [[i] + [min(i + lag_time, len(hospitalized)) for lag_time in lag_times] for i in reopening_indecies]

        lag_time_index_to_line = ['solid', 'dashed', 'dotted']

        for i in range(len(spike_expectations)):
            for j in range(len(spike_expectations[i])):
                plt.axvline(x=spike_expectations[i][j], color=colors[i], linestyle=lag_time_index_to_line[j], label=new_names[i][j])
        
        # print(names)
        # print(spike_expectations)

    window = 7
    doubling_times = [0] * window + [doubling_time(x, hospitalized, window) for x in range(window, len(hospitalized))]
    moving_average_window = 7
    doubling_times_moving_average = [0] * window + [np.mean(doubling_times[x - window: x]) for x in range(window, len(doubling_times))]

    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), len(dates)//7 - 1):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Doubling Time (Days)")
    plt.title(f"COVID-19 Hospitalization Doubling Time (7-Day Moving Avg) - {state}\nUsed covidtracking.com/api - Some data may be innacurate")
    plt.plot(doubling_times_moving_average, label="Doubling Time (7-Day Moving Average)")
    # plt.legend()
    # plt.show()
    plt.savefig(os.path.join("Graphs", "DoublingTime", f"{states_dict[state]}.png"))
    plt.cla()

    if state == "Florida":
        colors = ['r', 'y', 'g']
        exponential_doublings = [[i[0]-7, max(doubling_times[min(i[0]-7, 0):min(i[0] + 30, len(hospitalized))])] for i in spike_expectations]
        plt.plot(hospitalized, label="Actual Cumulative Hospitalizations")

        # print(exponential_doublings)

        x = [range(i[0], len(hospitalized)) for i in exponential_doublings]
        y = [[hospitalized[i] * 2 ** ((time - i)/doubling) for time in range(i, len(hospitalized))] for i, doubling in exponential_doublings]
        
        print(y)

        for i in range(len(x)):
            plt.plot(x[i], y[i], color=colors[i], label = f"Predicted Hospitalizations (No {names[i]} Reopening)", linestyle="dashed")

        plt.xlabel("Dates")
        plt.ylabel("Cumulative Hospitalizations")
        plt.title(f"COVID-19 Cumulative Hospitalizations - {state}\nUsed covidtracking.com/api - Some data may be innacurate")
        plt.savefig(os.path.join("Graphs", "DoublingTime", f"{states_dict[state]} PREDICTION.png"))
        # plt.legend()
        plt.show()
        plt.cla()
        # for i in range(len(hospitalized)):
        #    print(dates[i], doubling_time[i])