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
    return count > 30


# data is list of current hospitalization by day starting with day one
# window is average hospital stay time
def getCumulativeHospitalizations(data, window=5):
    total_hospitalizations = [data[0]]
    new_people = [data[0]/window]
    for index in range (1, window):
        new_people.append(data[0]/window)
    for index in range(1, len(data)):
        new_people.append(data[index] - (data[index - 1]) + new_people[index])
        total_hospitalizations.append(total_hospitalizations[index - 1] + new_people[index + window - 1])
    return total_hospitalizations


# file = open("../RawData/Illinois/il_covid_track_api_data.csv")
# data = file.read()
# def split(string):
#     num = string.split(",")[6]
#     if num != "":
#         return float(num)


# rows = data.split("\n")
# rows.pop(0)
# rows.remove('')
# rows = rows[::-1]
# numbers = []
# for row in rows:
#     num = row.split(",")[6]
#     if num != "":
#         numbers.append(float(num))

# print(numbers)
# print(getCumulativeHospitalizations(numbers))
