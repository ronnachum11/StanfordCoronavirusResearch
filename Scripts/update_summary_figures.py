import cv2
import os 
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

for state in states_dict:
    print(state)
    save_folder = os.path.join(path, "Graphs", "Analysis", state)
    if not os.path.isdir(save_folder):
        continue

    names = ["1CurrentHospitalizations.png", "2CumulativeHospitalizations.png", "3DoublingTimes.png", "4reopenings.png", "4reopenings_with_lag_times.png", "5doubling_times_reopenings.png", "6doubling_times_negative_reopenings.png", "7negative_reopenings.png", "8predictions.png"]
    imgs = [cv2.resize(cv2.imread(os.path.join(save_folder, name)), (900, 450)) for name in names[3:]]

    image = np.concatenate((imgs[0], imgs[1], imgs[2], imgs[3], imgs[4], imgs[5]), axis=0)
    cv2.imwrite(os.path.join(save_folder, "1Asummary_pic.png"), image)