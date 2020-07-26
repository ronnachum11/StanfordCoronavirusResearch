# This current structure is inefficent but allows for modularity so I am leaving it as is for the moment 
# If you only want to update a few of these, you can comment out the ones you don't want to update and run the script

text = ["", "Raw Data", "Cumulative Hospitalizations", "Current Hospitalizations", "Net Hospitalizations", "New Hospitalizations", "Doubling Times", "Analysis"]
i, length = 0, 7

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