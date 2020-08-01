from scipy import stats
import numpy as py

# NOTE: function only works for file in covid tracker api format
# file_contents is contents of the file in covid tracker api format
# min_count is minimum number of nescessary data points.
def hasCumulativeHospitalizations(file_contents, min_count=30):
    def split(string):
        return string.split(",")

    rows = file_contents.split("\n")
    rows = list(map(split, rows))
    rows.remove([""])
    count = 0
    for row in rows:
        count += (row[7] != "")
    return count > min_count


# data is list of current hospitalization by day starting with day one
# window is average hospital stay time
def getCumulativeHospitalizations(data, window=10):
    total_hospitalizations = [int(data[0] * 2)]
    new_people = [data[0]/window]
    for index in range(1, window):
        new_people.append(round(data[0]/window))
    for index in range(1, len(data)):
        new_people.append(data[index] - (data[index - 1]) + new_people[index])
        total_hospitalizations.append(max(total_hospitalizations[index - 1] + new_people[index + window - 1], 0))
    return total_hospitalizations

def findAverageStay(current, cumulative):

    left = []
    for index in range(0, len(cumulative)):
        if index + 1 < len(cumulative) and index + 1 < len(current):
            left.append(cumulative[index] - cumulative[index + 1] + current[index + 1] - current[index])

        else:
            break
    days = []
    total_days = len(left)
    for index in range(0, len(left)):
        if(index + 1 < len(current)):
            if(left[index] != 0):
                days.append(current[index + 1]/left[index])
        else:
            total_days -= 1

    z_scores = py.abs(stats.zscore(days))
    remove = py.where(z_scores > 3)
    print(remove)
    average = 0;
    for day in days:
        average += day

    return average / total_days

def findAverageStayTwo(current, cumulative, shift = 0):
    average = 0
    count = 0
    for index in range(0, len(cumulative)):
        if index < len(cumulative) and index + shift < len(current):
            print("{} , {}".format(current[index], cumulative[index]))
            average += cumulative[index] / (cumulative[index] - current[index + shift])
            count += 1
        else:
            break
    return average/count




# file = open("../RawData/South Dakota/sd_covid_track_api_data.csv")
# data = file.read()
# def split(string):
#     num = string.split(",")[6]
#     if num != "":
#         return float(num)





# rows = data.split("\n")
# rows.pop(0)
# rows.remove('')
# rows.reverse()
# curNumbers = []
# cumNumbers = []
# for row in rows:
#     cur = row.split(",")[6]
#     cum = row.split(",")[7]
#     if cur != "":
#         curNumbers.append(float(cur))
#     if cum != "":
#         cumNumbers.append(float(cum))
#
#
# guesses = getCumulativeHospitalizations(curNumbers)
# guesses.reverse()
# cumNumbers.reverse()
# curNumbers.reverse()
#
# #print(findAverageStay(curNumbers, cumNumbers))
# #print(findAverageStayTwo(curNumbers, cumNumbers))
# #print(guesses)
# #print(curNumbers)
# #print(cumNumbers[0:(len(curNumbers)-1)])
#
# finalIndex = len(guesses);
# percentAverage = 0
# for index in range(0, len(guesses)):
#
#     if(index >= len(cumNumbers)):
#         finalIndex = index - 1
#         break
#     percentAverage += abs((guesses[index] - cumNumbers[index]) / cumNumbers[index])
# print(percentAverage/finalIndex)
# averageError = 0
# states = 0
# rSquared = 0
#
# states_dict = {
#     'Alabama': 'AL',
#     'Alaska': 'AK',
#     'American Samoa': 'AS',
#     'Arizona': 'AZ',
#     'Arkansas': 'AR',
#     'California': 'CA',
#     'Colorado': 'CO',
#     'Connecticut': 'CT',
#     'Delaware': 'DE',
#     'District of Columbia': 'DC',
#     'Florida': 'FL',
#     'Georgia': 'GA',
#     'Guam': 'GU',
#     'Hawaii': 'HI',
#     'Idaho': 'ID',
#     'Illinois': 'IL',
#     'Indiana': 'IN',
#     'Iowa': 'IA',
#     'Kansas': 'KS',
#     'Kentucky': 'KY',
#     'Louisiana': 'LA',
#     'Maine': 'ME',
#     'Maryland': 'MD',
#     'Massachusetts': 'MA',
#     'Michigan': 'MI',
#     'Minnesota': 'MN',
#     'Mississippi': 'MS',
#     'Missouri': 'MO',
#     'Montana': 'MT',
#     'Nebraska': 'NE',
#     'Nevada': 'NV',
#     'New Hampshire': 'NH',
#     'New Jersey': 'NJ',
#     'New Mexico': 'NM',
#     'New York': 'NY',
#     'North Carolina': 'NC',
#     'North Dakota': 'ND',
#     'Northern Mariana Islands':'MP',
#     'Ohio': 'OH',
#     'Oklahoma': 'OK',
#     'Oregon': 'OR',
#     'Pennsylvania': 'PA',
#     'Puerto Rico': 'PR',
#     'Rhode Island': 'RI',
#     'South Carolina': 'SC',
#     'South Dakota': 'SD',
#     'Tennessee': 'TN',
#     'Texas': 'TX',
#     'Utah': 'UT',
#     'Vermont': 'VT',
#     'Virgin Islands': 'VI',
#     'Virginia': 'VA',
#     'Washington': 'WA',
#     'West Virginia': 'WV',
#     'Wisconsin': 'WI',
#     'Wyoming': 'WY'
# }
#
# for state in states_dict:
#
#     file = open("../RawData/{}/{}_covid_track_api_data.csv".format(state, states_dict[state].lower()))
#     data = file.read()
#
#     if hasCumulativeHospitalizations(data):
#         def split(string):
#             num = string.split(",")[6]
#             if num != "":
#                 return float(num)
#
#         rows = data.split("\n")
#         rows.pop(0)
#         rows.remove('')
#         rows.reverse()
#         curNumbers = []
#         cumNumbers = []
#         for row in rows:
#             cur = row.split(",")[6]
#             cum = row.split(",")[7]
#             if cur != "":
#                 curNumbers.append(float(cur))
#             if cum != "":
#                 cumNumbers.append(float(cum))
#
#         guesses = getCumulativeHospitalizations(curNumbers)
#         guesses.reverse()
#         cumNumbers.reverse()
#         curNumbers.reverse()
#
#
#         finalIndex = len(guesses);
#         percentAverage = 0
#         for index in range(0, len(guesses)):
#
#             if(index >= len(cumNumbers)):
#                 finalIndex = index - 1
#                 break
#             if(cumNumbers[index] != 0):
#                 percentAverage += abs((guesses[index] - cumNumbers[index]) / cumNumbers[index])
#         if finalIndex != 0:
#             if percentAverage/finalIndex < 1:
#                 rSquared += (percentAverage/finalIndex)**2
#                 averageError += percentAverage/finalIndex
#                 states += 1
#             print("days:{} error:{}".format(findAverageStay(curNumbers, cumNumbers), percentAverage/finalIndex))
#
# print(averageError/states)
# print(rSquared/states)