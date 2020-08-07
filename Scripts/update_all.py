# Run this script to update all data and graphs
import matplotlib.pyplot as plt 
plt.style.use('ggplot')

text = ["", "Raw Data", "Cumulative Hospitalizations", "Current Hospitalizations", "Net Hospitalizations", "New Hospitalizations", "Doubling Times", "Analysis", "Summary Figures"]
i, length = 0, 8

i +=1; print(f"Task {i}/{length}: Updating {text[i]}")
import update_covidtracking_data
i +=1; print(f"Task {i}/{length}: Updating {text[i]}")
import update_cumulative_hospitalizations
i +=1; print(f"Task {i}/{length}: Updating {text[i]}")
import update_current_hospitalizations
i +=1; print(f"Task {i}/{length}: Updating {text[i]}")
import update_net_hospitalizations
i +=1; print(f"Task {i}/{length}: Updating {text[i]}")
import update_new_hospitalizations
i +=1; print(f"Task {i}/{length}: Updating {text[i]}")
import update_doubling_time
i +=1; print(f"Task {i}/{length}: Updating {text[i]}")
import update_analysis
i +=1; print(f"Task {i}/{length}: Updating {text[i]}")
import update_summary_figures