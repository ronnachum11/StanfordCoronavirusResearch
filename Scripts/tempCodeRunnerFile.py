import os
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('ggplot')
path = "C:\\Users\\Ron\\StanfordCoronavirusResearch"

reopening_df = pd.read_csv(os.path.join(path, "RawData", "StateReopening", "FinalData.csv"))
reopening_df = reopening_df.drop(reopening_df.columns[15:], axis=1)
headers = list(reopening_df.columns)
reopening_effects = [[] for i in range(len(headers) - 1)]

# reopening_effects_means = [np.mean(i) for i in reopening_effects]
# reopening_effects_medians = [statistics.median(i) if len(i) != 0 else 0 for i in reopening_effects]
reopening_effects_medians = [142.55833220698725, -56.78712956375391, 67.92439695284196, 235.96976582978823, -51.21215236715598, -15.902850889595321, 52.79181876967962, 3.529595232480176, 26.866600337157, -53.20459867493015, 51.92371443199131, 106.7916322663877, 34.845353470126895, 103.85087493482499]
# print(reopening_effects_means)
# print(reopening_effects_medians)

reopenings_with_headers = zip(reopening_effects_medians, headers[1:])
reopenings_with_headers = sorted(reopenings_with_headers, key=lambda x: -1*x[0])
# print(reopenings_with_headers)

negative_reopenings = [x[0] for x in reopenings_with_headers if x[0] < 0]
positive_reopenings = [x[0] for x in reopenings_with_headers if x[0] >= 0]
print(len(negative_reopenings), len(positive_reopenings))
headers = [x[1] for x in reopenings_with_headers]

plt.title("Reopening Orders Effect on Doubling Time")
plt.xlabel("Reopening Type")
plt.ylabel("Median Change Before/After Reopening (%)")
plt.xticks(range(len(headers)), headers, rotation=90)
plt.bar(range(len(positive_reopenings)), positive_reopenings, color="g")
plt.bar(range(len(positive_reopenings), len(headers)), negative_reopenings, color="r")
plt.savefig(os.path.join(path, "Graphs", "Analysis", "ReopeningData.png"), bbox_inches='tight')
# plt.show()