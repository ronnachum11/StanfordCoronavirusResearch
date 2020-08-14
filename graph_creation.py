import pandas as pd
import os
import math
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np 
import time
import statistics 
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.tools as tls

from current_to_cumulative import hasCumulativeHospitalizations, getCumulativeHospitalizations
import logging
logging.getLogger().setLevel(logging.CRITICAL)

plt.style.use('ggplot')

alpha = 1
lag_time = 14
doubling_time_window=7

# path = "C:\\Users\\Ron\\StanfordCoronavirusResearch"

states_dict = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
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
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
path = "C:\\Users\\Ron\\StanfordCoronavirusResearch"
colors = ['red', 'orangered', 'yellow', 'gold', 'lime', 'green', 'cyan', 'deepskyblue', 'blue', 'violet', 'purple', 'indigo', 'gray', 'black', 'peru']

reopening_df = pd.read_excel(os.path.join("RawData", "StateReopening", "FinalData.xlsx"))
reopening_df = reopening_df.drop(reopening_df.columns[15:], axis=1)

headers = list(reopening_df.columns)

def moving_average(lst, cumulative=True, window=7):
    if len(lst) < window:
        return lst
    
    lst = lst[:window] + [np.mean(lst[i-window:i]) for i in range(window, len(lst))]

    if cumulative:
        lst = [lst[0]] + [max(lst[:i]) for i in range(1, len(lst))]

    return lst

def doubling_time(m, y, window):
    y1, y2 = y[m - window], y[m]

    if y1 == 0:
        return 0

    return (window) * np.log(2) / np.log(y2 / y1)

def clean_reopening_dates(reopening_dates):
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
    return reopening_dates

def clean_hospitalizations(state, hospitalized, dates, state_df):
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
    # problem_states = ["Alabama", "Arizona", "Alaska", "Connecticut", "Delaware", 
    #               "Indiana", "Iowa", "Missouri", "New Hampshire", "Pennsylvania",
    #               "Vermont", "West Virginia", ""]
    problem_states = ["Arizona", "Pennsylvania"]
    if len(hospitalized) < window or state in problem_states:
        current_hospitalizations = list(state_df['hospitalizedCurrently'])[::-1]
        dates = list(state_df['date'])[::-1]

        dates = [dates[i] for i in range(len(dates)) if not math.isnan(current_hospitalizations[i])]
        current_hospitalizations = [i for i in current_hospitalizations if not math.isnan(i)]
        
        for i in range(1, len(current_hospitalizations)):
            if math.isnan(current_hospitalizations[i]):
                current_hospitalizations[i] = current_hospitalizations[i-1]

        if len(current_hospitalizations) > window:
            hospitalized = getCumulativeHospitalizations(current_hospitalizations, window)
            calculated = True

    hospitalized = moving_average(hospitalized)
    return hospitalized, dates, calculated

def get_doubling_time_data(hospitalized, doubling_time_window=7, moving_average_window=7):
    doubling_times = [0] * doubling_time_window + [doubling_time(x, hospitalized, doubling_time_window) for x in range(doubling_time_window, len(hospitalized))]
    for i in range(1, len(doubling_times)):
        if math.isinf(doubling_times[i]):
            doubling_times[i] = doubling_times[i-1]
    
    doubling_times_moving_average = [0] * moving_average_window + [np.mean(doubling_times[x - moving_average_window: x]) for x in range(moving_average_window, len(doubling_times))]
    doubling_times_derivative = [0] + [doubling_times_moving_average[i] - doubling_times_moving_average[i-1] for i in range(1, len(doubling_times_moving_average))]
    return doubling_times, doubling_times_moving_average, doubling_times_derivative

def get_xticks(dates):
    x_ticks, x_tick_labels = [], []
    for i in range(0, len(dates), len(dates)//7 - 1):
        date = str(dates[i])
        x_ticks.append(i)
        x_tick_labels.append(date[4:6] + "/" + date[6:8])
    return x_ticks, x_tick_labels

def plotly_plot(info, d, title, save_name, plot_reopenings=False, plot_spike_expectations=False, plot_predictions=False, negative_only=False):
    df, state, x_ticks, x_tick_labels, reopening_indecies, spike_expectations, names, x, y, exponential_doublings, hospitalized = info

    data = ["Cumulative COVID-19 Hospitalizations", "Hospitalization Doubling Time (Days)", "Hospitalization Doubling Time Rate of Change (Days/Day)"]
    d = data[d]

    fig = px.line(df, x="Dates", y=d, title=f"{title} - {state}")
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = x_ticks,
            ticktext = x_tick_labels
        ),
        hovermode="x unified",
    )

    if plot_reopenings:
        for num, i in enumerate(reopening_indecies):
            if i is not None and (not negative_only or exponential_doublings[num] is not None and y[num][-1] < hospitalized[-1]):
                fig.add_trace(go.Scatter(x=[i, i], y=[min([0] + list(df[d])), max(list(df[d]))], mode="lines", 
                            name=names[num] + " Reopening", line=dict(color=colors[num])))
    
    if plot_spike_expectations:
        for num, i in enumerate(spike_expectations):
            if i is not None and (not negative_only or exponential_doublings[num] is not None and y[num][-1] < hospitalized[-1]):
                fig.add_trace(go.Scatter(x=[i, i], y=[min([0] + list(df[d])), max(list(df[d]))], mode="lines", 
                    name=names[num] + " Spike Expectation", line=dict(color=colors[num], dash='dot')))
    
    if plot_predictions:
        for i in range(len(x)):
            if x[i] is not None:
                if y[i][-1] < hospitalized[-1]:
                    fig.add_trace(go.Scatter(x=list(x[i]), y=y[i], mode="lines", name=names[i] + " Non-Reopening Trajectory",
                                  line=dict(color=colors[i], dash='dash')))

    fig.write_html(os.path.join('application', 'static', 'graphs', state, save_name), full_html=False, include_plotlyjs=False)

def update_graphs(state):
    print(state)
    # fig = plt.figure()
    save_folder = os.path.join("application", "static", "graphs", state)
    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)
    
    state_df = pd.read_csv(f"https://covidtracking.com/api/v1/states/{states_dict[state].lower()}/daily.csv")
    # state_df = pd.read_csv(os.path.join(path, "RawData", state, f"{states_dict[state].lower()}_covid_track_api_data.csv"))
    hospitalized = list(state_df['hospitalizedCumulative'])[::-1]
    dates = list(state_df['date'])[::-1]

    reopening_dates = []
    for i, row in reopening_df.iterrows():
        if list(row)[0] == state:
            reopening_dates = list(row)[1:]

    reopening_dates = clean_reopening_dates(reopening_dates)
    hospitalized, dates, calculated = clean_hospitalizations(state, hospitalized, dates, state_df)
    doubling_times, doubling_times_moving_average, doubling_times_derivative = get_doubling_time_data(hospitalized, doubling_time_window)
    x_ticks, x_tick_labels = get_xticks(dates)

    df = pd.DataFrame({"Dates": range(len(hospitalized)), "Date Values": dates,
                      "Cumulative COVID-19 Hospitalizations": hospitalized, 
                      "Hospitalization Doubling Time (Days)": doubling_times_moving_average,
                      "Hospitalization Doubling Time Rate of Change (Days/Day)": doubling_times_derivative })

    names, reopening_dates = headers[1:], reopening_dates
    reopening_indecies = [dates.index(i) if i is not None and i in dates else None for i in reopening_dates]
    spike_expectations = [min(i + lag_time, len(hospitalized)) if i is not None else None for i in reopening_indecies]

    for i, index in enumerate(reopening_indecies):
        if index is not None and index in reopening_indecies[:i]:
            nums_to_try = [1, -1, 2, -2, 3, -3, 4, -4, 5, -5]
            original_index = index; count = 0
            while index in reopening_indecies[:i]:
                index = original_index + nums_to_try[count]
                count += 1
            reopening_indecies[i] += nums_to_try[count-1]
            spike_expectations[i] += nums_to_try[count-1]

    exponential_doublings = [[i, doubling_times_moving_average[i + lag_time]] if i is not None and i + lag_time*1.5 < len(doubling_times_derivative) and np.mean(doubling_times_derivative[i + lag_time:min(i + lag_time*2, len(doubling_times_derivative))]) < np.mean(doubling_times_derivative[i:i+lag_time]) else None for i in reopening_indecies]
    x = [range(i[0], len(hospitalized)) if i is not None else None for i in exponential_doublings]
    y = [[hospitalized[doubling[0]] * (2 ** ((time - doubling[0])/doubling[1])) for time in range(doubling[0], len(hospitalized))] if doubling is not None else None for doubling in exponential_doublings]
    
    info = [df, state, x_ticks, x_tick_labels, reopening_indecies, spike_expectations, names, x, y, exponential_doublings, hospitalized]

    if not os.path.isdir(os.path.join('application', 'static', 'graphs', state)):
        os.mkdir(os.path.join('application', 'static', 'graphs', state))

    plotly_plot(info, 0, "COVID-19 Cumulative Hospitalizations", "Acumulative_hospitalizations.html")
    plotly_plot(info, 1, "COVID-19 Doubling Time", "Bdoubling_times.html")
    plotly_plot(info, 0, "COVID-19 Cumulative Hospitalizations + Reopenings", "Creopenings.html", True)
    plotly_plot(info, 1, "COVID-19 Doubling Time + Spike Expectations", "Dreopenings_spikes.html", False, True)
    plotly_plot(info, 0, "COVID-19 Cumulative Hospitalizations + Negative Reopenings", "Enegative_reopenings.html", True, negative_only=True)
    plotly_plot(info, 0, "COVID-19 Cumulative Hospitalizations + Non-Reopening Trajectory Predictions", "Fpredictions.html", True, negative_only=True, plot_predictions=True)

def update_all_graphs():
    for state in states_dict:
        update_graphs(state)

if __name__ == "__main__":
    # update_graphs("California")

    start = time.time()
    update_all_graphs()
    print(time.time() - start)