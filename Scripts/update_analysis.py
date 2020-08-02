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

alpha = 1
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

def doubling_time(m, y, window):
    y1, y2 = y[m - window], y[m]

    if y1 == 0:
        return 0

    return (window) * np.log(2) / np.log(y2 / y1)

for state in states_dict:
    # print(state)
    save_folder = os.path.join(path, "Graphs", "Analysis", state)
    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)
    
    state_data = pd.read_csv(os.path.join(path, "RawData", state, f"{states_dict[state].lower()}_covid_track_api_data.csv"))
    hospitalized = list(state_data['hospitalizedCumulative'])[::-1]
    dates = list(state_data['date'])[::-1]

    reopening_dates = []
    for i, row in reopening_df.iterrows():
        if list(row)[0] == state:
            reopening_dates = list(row)[1:]

    for i, date in enumerate(reopening_dates):
        if isinstance(date, str):
            date = date.split(" ")[0]
            date = '2020' + '0' * (4 - len(date)) + date
            reopening_dates[i] = int(date)
        elif not math.isnan(date):
            date = str(int(date))
            date = '2020' + '0' * (4 - len(date)) + date
            reopening_dates[i] = int(date)
        else:
            reopening_dates[i] = None

    # print(reopening_dates)

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
        # print(state)
        current_hospitalizations = list(state_data['hospitalizedCurrently'])[::-1]
        dates = list(state_data['date'])[::-1]

        dates = [dates[i] for i in range(len(dates)) if not math.isnan(current_hospitalizations[i])]
        current_hospitalizations = [i for i in current_hospitalizations if not math.isnan(i)]

        for i in range(1, len(current_hospitalizations)):
            if math.isnan(current_hospitalizations[i]):
                current_hospitalizations[i] = current_hospitalizations[i-1]

        if len(current_hospitalizations) > window:
            hospitalized = getCumulativeHospitalizations(current_hospitalizations, window)
            calculated = True

    hospitalized = moving_average(hospitalized)

    window = 7
    doubling_times = [0] * window + [doubling_time(x, hospitalized, window) for x in range(window, len(hospitalized))]
    moving_average_window = 7
    doubling_times_moving_average = [0] * window + [np.mean(doubling_times[x - window: x]) for x in range(window, len(doubling_times))]
    doubling_times_derivative = [0] + [doubling_times_moving_average[i] - doubling_times_moving_average[i-1] for i in range(1, len(doubling_times_moving_average))]

    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), len(dates)//7 - 1):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])

    names, reopening_dates = headers, reopening_dates
    lag_time = 28

    colors = ['red', 'orangered', 'yellow', 'gold', 'lime', 'green', 'cyan', 'deepskyblue', 'blue', 'violet', 'purple', 'indigo', 'gray', 'black', 'peru']
    reopening_indecies = [dates.index(i) if i is not None and i in dates else None for i in reopening_dates]
    # print(dates)
    spike_expectations = [min(i + lag_time, len(hospitalized)) if i is not None else None for i in reopening_indecies]

    exponential_doublings = [[i, doubling_times_moving_average[i + lag_time]] if i is not None and i + lag_time*2 < len(doubling_times_derivative) and np.mean(doubling_times_derivative[i + lag_time:i + lag_time*2]) < np.mean(doubling_times_derivative[i:i+lag_time]) else None for i in reopening_indecies]
    
    for num, index in enumerate(reopening_indecies):
        if index is not None and num + lag_time*2 < len(doubling_times_derivative):
            pre = np.mean(doubling_times_derivative[index:index + lag_time])
            post = np.mean(doubling_times_derivative[index + lag_time:index + lag_time*2])
            # print(pre, post)
            if not math.isnan(pre) and not math.isnan(post):
                reopening_effects[num].append((post - pre / pre)*100)

    for num, index in enumerate(reopening_indecies):
        if index is not None:
            plt.axvline(x=index, linestyle='solid', label=names[num] + " Reopening", color=colors[num], alpha=alpha)
    for num, index in enumerate(spike_expectations):
        if index is not None:
            plt.axvline(x=index, linestyle='dotted', color=colors[num], alpha=alpha)
    plt.plot(hospitalized, color='k', label='Actual Hospitalizations')
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Cumulative COVID-19 Hospitalizations")
    if not calculated:
        plt.title(f"Reopenings - {state}")
    else:
        plt.title(f"Reopenings - {state} (Calc)")
    plt.savefig(os.path.join(save_folder, "4reopenings.png"), bbox_inches='tight')
    plt.clf()

    plt.plot(hospitalized, color="k")
    x = [range(i[0], len(hospitalized)) if i is not None else None for i in exponential_doublings]
    y = [[hospitalized[doubling[0]] * (2 ** ((time - doubling[0])/doubling[1])) for time in range(doubling[0], len(hospitalized))] if doubling is not None else None for doubling in exponential_doublings]
    
    for i in range(len(x)):
        if x[i] is not None:
            if y[i][-1] < hospitalized[-1]:
                plt.plot(x[i], y[i], color=colors[i], linestyle="dashed")
                added_hospitalizations[i].append(hospitalized[-1] - y[i][-1])# (hospitalized[-1] - y[i][-1])/y[i][-1])
                if exponential_doublings[i] is not None:
                    plt.axvline(x=reopening_indecies[i], linestyle='solid', label=names[i] + " Reopening", color=colors[i], alpha=alpha) 
                    plt.axvline(x=spike_expectations[i], linestyle='dotted', color=colors[i], alpha=alpha)

    # print(state, hospitalized)

    if not calculated:
        plt.title(f"Predicted Trajectories Without Reopenings - {state}")
    else:
        plt.title(f"Predicted Trajectories Without Reopenings - {state} (Calc)")

    # plt.legend()
    # plt.savefig(os.path.join(save_folder, "8predictions.png"), bbox_inches='tight')
    # plt.show()
    plt.clf()

    for num, index in enumerate(reopening_indecies):
        if index is not None:
            plt.axvline(x=index, linestyle='solid', label=names[num] + " Reopening", color=colors[num], alpha=alpha)
    for num, index in enumerate(spike_expectations):
        if index is not None:
            plt.axvline(x=index, linestyle='dotted', color=colors[num], alpha=alpha)

    if not calculated:
        plt.title(f"Reopenings - {state}")
    else:
        plt.title(f"Reopenings - {state} (Calc)")
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Doubling Time (Days)")
    if not calculated:
        plt.title(f"Reopenings - {state}")
    else:
        plt.title(f"Reopenings - {state} (Calc)")
    # plt.plot(doubling_times, label="Doubling Time")
    plt.plot(doubling_times_moving_average, label="Doubling Time (7-Day Moving Average)", color='k')
    # plt.savefig(os.path.join(save_folder, "5doubling_times_reopenings.png"), bbox_inches='tight')
    plt.clf()

    for num, index in enumerate(reopening_indecies):
        if exponential_doublings[num] is not None and y[num][-1] < hospitalized[-1]:
            plt.axvline(x=index, linestyle='solid', label=names[num] + " Reopening", color=colors[num], alpha=alpha)
    for num, index in enumerate(spike_expectations):
        if exponential_doublings[num] is not None and y[num][-1] < hospitalized[-1]:
            plt.axvline(x=index, linestyle='dotted', color=colors[num], alpha=alpha)
    plt.plot(hospitalized, color='k', label='Actual Hospitalizations')
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Cumulative COVID-19 Hospitalizations")
    if not calculated:
        plt.title(f"Reopenings With Negative Effects - {state}")
    else:
        plt.title(f"Reopenings With Negative Effects - {state} (Calc)")
    # print(len(hospitalized), len(doubling_times_moving_average), len(doubling_times_derivative))
    # plt.savefig(os.path.join(save_folder, "7negative_reopenings.png"), bbox_inches='tight')
    plt.clf()

    for num, index in enumerate(reopening_indecies):
        if exponential_doublings[num] is not None and y[num][-1] < hospitalized[-1]:
            plt.axvline(x=index, color=colors[num], linestyle='solid', label=names[num] + " Reopening", alpha=alpha)
    for num, index in enumerate(spike_expectations):
        if exponential_doublings[num] is not None and y[num][-1] < hospitalized[-1]:
            plt.axvline(x=index, color=colors[num], linestyle='dotted', alpha=alpha)

    # plt.show()
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel("Dates")
    plt.ylabel("Doubling Time (Days)")
    if not calculated:
        plt.title(f"Reopenings With Negative Effects - {state}")
    else:
        plt.title(f"Reopenings With Negative Effects - {state} (Calc)")
    # plt.plot(doubling_times, label="Doubling Time")
    plt.plot(doubling_times_moving_average, label="Doubling Time (7-Day Moving Average)", color='k')
    # plt.savefig(os.path.join(save_folder, "6doubling_times_negative_reopenings.png"), bbox_inches='tight')
    plt.clf()

reopening_effects_means = [np.mean(i) for i in reopening_effects]
reopening_effects_medians = [statistics.median(i) if len(i) != 0 else 0 for i in reopening_effects]
# print(reopening_effects_means)
# print(reopening_effects_medians)

for i in [["Median", reopening_effects_medians]]: # ["Mean", reopening_effects_means]]:
    title, data = i
    
    reopenings_with_headers = zip(data, headers[1:])
    reopenings_with_headers = sorted(reopenings_with_headers, key=lambda x: -1*x[0])
    print(reopenings_with_headers)
    # print(reopenings_with_headers)

    negative_reopenings = [x[0] for x in reopenings_with_headers if x[0] < 0]
    positive_reopenings = [x[0] for x in reopenings_with_headers if x[0] >= 0]
    print(len(negative_reopenings), len(positive_reopenings))
    labels = [x[1] for x in reopenings_with_headers]

    plt.title("Reopening Orders Effect on Doubling Time")
    plt.xlabel("Reopening Type")
    plt.ylabel(f"{title} Change Before/After Reopening (%)")
    plt.xticks(range(len(labels)), labels, rotation=90)
    plt.bar(range(len(positive_reopenings)), positive_reopenings, color="g")
    plt.bar(range(len(positive_reopenings), len(labels)), negative_reopenings, color="r")
    plt.savefig(os.path.join(path, "Graphs", "Analysis", f"ReopeningData{title}-{lag_time}.png"), bbox_inches='tight')
    # plt.show()

added_hospitalizations = [sum(x) if len(x) > 0 else 0 for x in added_hospitalizations]
print(sorted(zip(headers[1:], added_hospitalizations), key = lambda x: -1*x[1]))
