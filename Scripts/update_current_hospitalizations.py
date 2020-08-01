import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import os 
import math
from utils import moving_average

r = requests.get("https://covidtracking.com/api/v1/states/daily.json")

# print(r.status_code)

with open('data.json', 'w') as f:
    json.dump(r.json(), f)

data = pd.read_json("data.json")
states = set(data['state'])
states = sorted(states)

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

states_dict = {states_dict[s]: s for s in states_dict}

# print(data.columns)
for state in states:
    state_data = data.loc[data['state'] == state]
    hospitalized = list(state_data['hospitalizedCurrently'])[::-1]
    dates = list(state_data['date'])[::-1]

    dates = [dates[i] for i in range(len(dates)) if not math.isnan(hospitalized[i])]
    hospitalized = [i for i in hospitalized if not math.isnan(i)]

    for i in range(1, len(hospitalized)):
        if math.isnan(hospitalized[i]):
            hospitalized[i] = hospitalized[i-1]

    hospitalized = moving_average(hospitalized)

    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), max(1, len(dates)//7 - 1)):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])
    
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Total Current Hospitalizations")
    plt.title(f"COVID-19 Current Hospitalizations - {state}")
    plt.plot(hospitalized, color='k')
    plt.savefig(os.path.join("Graphs", "General", "Current Hospitalizations", f"{state}.png"), bbox_inches='tight')
    plt.savefig(os.path.join("Graphs", "Analysis", states_dict[state], "1CurrentHospitalizations.png"), bbox_inches='tight')
    # plt.show()
    plt.cla()
# print(len(states))


