# Script to compare how projects do in different versions of osrank

import sys
import pandas as pd

# Expects the following arguments
# [0] filename of this script
# [1] filename of the output CSV
# [2] number of projects to keep from the first input CSV
# [3] path to primary input CSV, containing large number of winning projects
# [4]..[N] Paths to other input CSVs containing shorters lists of 'winning' projects
# Should be at least 2 CSV paths

# Make sure we have enough params
if (len(sys.argv) < 5):
  exit("Please pass the arguments we require (check the Python code)")

# Save output path
output_path = sys.argv[1]

# Save number of projects to keep
num_projects = int(sys.argv[2])

# Load other params into datafames (no error checking)
inputs = []
for path in sys.argv[3:-1]:
  df = pd.read_csv(path, header=None, names=["Name", "Osrank"]).head(num_projects)
  inputs.append({
    "path": path,
    "dataframe": df,
    "rank_series": []
  })

# Init comparison dataframe
compare = inputs[0]["dataframe"][["Name"]].copy()

# Build a series for each input, containing ranks of base input's winning projects
for index, row in inputs[0]['dataframe'].iterrows():
  for container in inputs:
    # this returns [] if the value is not present in the column
    this_rows_rank_in_this_dataframe = container["dataframe"].index[container["dataframe"]['Name']==row['Name']]
    rank = -1
    if len(this_rows_rank_in_this_dataframe) > 0:
      rank = this_rows_rank_in_this_dataframe[0] + 1 # start ranks at 1, not 0
    
    # now we're confident our rank is correct, or negative 1
    container["rank_series"].append(rank)

# For each input, add ranks to compare dataframe
for container in inputs:
  compare[container["path"]] = container["rank_series"]

compare.to_csv(output_path, index=False)
print(compare)