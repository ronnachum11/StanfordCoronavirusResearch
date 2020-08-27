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
    
    files = list(os.listdir(save_folder))
    names = ["1CurrentHospitalizations.png", "2CumulativeHospitalizations.png", "3DoublingTimes.png", "4reopenings.png", "4reopenings_with_lag_times.png", "5doubling_times_reopenings.png", "6doubling_times_negative_reopenings.png", "7negative_reopenings.png", "8predictions.png"]
    
    empty = np.zeros((460, 610, 3), dtype=np.uint8)
    empty.fill(255)

    imgs = [cv2.resize(cv2.imread(os.path.join(save_folder, name)), (610, 460)) for name in names[3:-1]]
    imgs2 = [cv2.resize(cv2.imread(os.path.join(save_folder, file)), (610, 460)) for file in files if "8predictions-" in file and "8predictions-all" not in file]

    imgs3 = [cv2.resize(cv2.imread(os.path.join(save_folder, name)), (610, 460)) for name in names[3:6]]
    imgs4 = [cv2.resize(cv2.imread(os.path.join(save_folder, name)), (610, 460)) for name in names[6:9]]
    image2 = None
    image3_pt1 = np.concatenate(imgs3, axis=1)
    image3_pt2 = np.concatenate(imgs4, axis=1)
    image3 = np.concatenate((image3_pt1, image3_pt2), axis=0)
    cv2.imwrite(os.path.join(save_folder, "1AAAcondensed_summary_pic.png"), image3)

    if len(imgs2) == 0:
        image = np.concatenate(imgs, axis=0)
    else:
        diff = len(imgs) - len(imgs2)
        print(len(imgs), len(imgs2), diff)
        if diff > 0:
            imgs2 = imgs2 + [empty]*diff
        else:
            diff *= -1
            imgs = imgs + [empty]*diff
        image1 = np.concatenate(imgs, axis=1)
        image2 = np.concatenate(imgs2, axis=1)
        image = np.concatenate((image1, image2), axis=0)
        
    cv2.imwrite(os.path.join(save_folder, "1AAsummary_pic.png"), image)
    if image2 is not None:
        cv2.imwrite(os.path.join(save_folder, "8predictions-all.png"), image2)

