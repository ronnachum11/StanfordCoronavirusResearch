import pandas as pd
import os
import math
import matplotlib.pyplot as plt
import numpy as np 
import time
import statistics 
from ConvertCurrentToCumulative import hasCumulativeHospitalizations, getCumulativeHospitalizations
from utils import moving_average 
plt.style.use('ggplot')

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

reopening_df = pd.read_excel(os.path.join(path, "RawData", "StateReopening", "FinalData.xlsx"))
reopening_df = reopening_df.drop(reopening_df.columns[15:], axis=1)
headers = list(reopening_df.columns)
reopening_effects = [[] for i in range(len(headers) - 1)]
added_hospitalizations = [[] for i in range(len(headers) - 1)]

colors = ['red', 'orangered', 'yellow', 'gold', 'lime', 'green', 'cyan', 'deepskyblue', 'blue', 'violet', 'purple', 'indigo', 'gray', 'black', 'peru']
for i in range(len(colors)):
    print(i)
    plt.plot([0], color=colors[i], label=headers[i+1])
plt.legend()
plt.savefig(os.path.join(path, "Graphs", "Analysis", "legend.png"))
plt.clf()