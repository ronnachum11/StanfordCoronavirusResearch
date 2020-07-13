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

    return (window) * np.log(2) / np.log(y2 / y1)

for state in states_dict:
    if state == "Florida":
        state_data = pd.read_csv(os.path.join(path, "RawData", state, f"{states_dict[state].lower()}_covid_track_api_data.csv"))

        hospitalized = list(state_data['hospitalizedCumulative'])[::-1]
        dates = list(state_data['date'])[::-1]
        
        num, count = hospitalized[0], 0
        while math.isnan(num):
            num = hospitalized[count]
            count += 1
        hospitalized, dates = hospitalized[count:], dates[count:]

        window = 14
        doubling_time = [0] * window + [doubling_time(x, hospitalized, window) for x in range(window, len(hospitalized))]

        x_ticks, x_tick_labels = [], []
        for i in range(0, len(dates), len(dates)//7 - 1):
            date = str(dates[i])
            x_ticks.append(i)
            x_tick_labels.append(date[4:6] + "/" + date[6:8])
        plt.xticks(x_ticks, x_tick_labels)
        plt.xlabel("Dates")
        plt.ylabel("Doubling Time (Days)")
        plt.title(f"COVID-19 Hospitalization Doubling Time - {state}\nUsed covidtracking.com/api - Some data may be innacurate")
        plt.plot(doubling_time, label="Doubling Time")
        plt.legend()
        plt.show()
        plt.cla()