import pandas as pd
import os
import math
import matplotlib.pyplot as plt
import numpy as np 
import time
from ConvertCurrentToCumulative import hasCumulativeHospitalizations, getCumulativeHospitalizations

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

reopening_df = pd.read_csv(os.path.join(path, "RawData", "StateReopening", "FinalData.csv"))
reopening_df = reopening_df.drop(reopening_df.columns[15:], axis=1)
headers = reopening_df.columns

def doubling_time(m, y, window):
    y1, y2 = y[m - window], y[m]

    if y1 == 0:
        return 0

    return (window) * np.log(2) / np.log(y2 / y1)

for state in states_dict:
    state_data = pd.read_csv(os.path.join(path, "RawData", state, f"{states_dict[state].lower()}_covid_track_api_data.csv"))
    hospitalized = list(state_data['hospitalizedCumulative'])[::-1]
    dates = list(state_data['date'])[::-1]

    reopening_data = reopening_df[reopening_df['State'] == state]
    # print(list(reopening_data))

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
    
    window = 7
    doubling_times = [0] * window + [doubling_time(x, hospitalized, window) for x in range(window, len(hospitalized))]
    moving_average_window = 7
    doubling_times_moving_average = [0] * window + [np.mean(doubling_times[x - window: x]) for x in range(window, len(doubling_times))]

    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), len(dates)//7 - 1):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])

    if state == "Florida":
        names, reopening_dates = ["Phase 1", "Phase 2"], [20200504, 20200605]
        lag_time = 14

        colors = ['r', 'y', 'g']
        reopening_indecies = [dates.index(i) for i in reopening_dates]
        # print(dates)
        spike_expectations = [min(i + lag_time, len(hospitalized)) for i in reopening_indecies]

        for num, index in enumerate(reopening_indecies):
            plt.axvline(x=index, color=colors[num], linestyle='solid', label=names[num] + " Reopening")
        for num, index in enumerate(spike_expectations):
            plt.axvline(x=index, color=colors[num], linestyle='dotted')

        exponential_doublings = [[i, doubling_times_moving_average[i + lag_time]] if i + lag_time < len(doubling_times_moving_average) and doubling_times_moving_average[i + lag_time] < max(doubling_times_moving_average[i:i+lag_time]) else None for i in reopening_indecies]

        x = [range(i[0], len(hospitalized)) if i is not None else None for i in exponential_doublings]
        y = [[hospitalized[i] * (2 ** ((time - i)/doubling[1])) for time in range(doubling[0], len(hospitalized))] if doubling is not None else None for doubling in exponential_doublings]
        
        for i in range(len(x)):
            if x[i] is not None:
                plt.plot(x[i], y[i], color=colors[i], linestyle="dashed")        
        
        plt.plot(hospitalized, color='k', label='Actual Hospitalizations')
        plt.xticks(x_ticks, x_tick_labels)
        plt.xlabel("Dates")
        plt.ylabel("Cumulative COVID-19 Hospitalizations")
        if not calculated:
            plt.title(f"COVID-19 Cumulative Hospitalizations - {state}\nUsed covidtracking.com/api - Some data may be innacurate")
        else:
            plt.title(f"COVID-19 Cumulative Hospitalizations - {state} (Calc)\nUsed covidtracking.com/api - Some data may be innacurate")

        plt.legend()
        plt.savefig(os.path.join("Graphs", "DoublingTime", f"{states_dict[state]}_Prediction.png"))
        plt.clf()

        for num, index in enumerate(reopening_indecies):
            plt.axvline(x=index, color=colors[num], linestyle='solid', label=names[num] + " Reopening")
        for num, index in enumerate(spike_expectations):
            plt.axvline(x=index, color=colors[num], linestyle='dotted')

    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Doubling Time (Days)")
    if not calculated:
        plt.title(f"COVID-19 Hospitalization Doubling Time (7-Day Moving Avg) - {state}\nUsed covidtracking.com/api - Some data may be innacurate")
    else:
        plt.title(f"COVID-19 Hospitalization Doubling Time (Moving Avg) - {state} (Calc)\nUsed covidtracking.com/api - Some data may be innacurate")
    # plt.plot(doubling_times, label="Doubling Time")
    plt.plot(doubling_times_moving_average, label="Doubling Time (7-Day Moving Average)")
    plt.legend()
    # plt.show()
    plt.savefig(os.path.join("Graphs", "DoublingTime", f"{states_dict[state]}.png"))
    plt.clf()