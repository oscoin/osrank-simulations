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
for path in sys.argv[3:]:
  df = pd.read_csv(path)
  if (num_projects>0):
    df = df.head(num_projects)
  if (len(df.columns) == 2):
    df.columns = ['Name', 'Osrank']
  elif (len(df.columns) == 3):
    df.columns = ['Name', 'Id', 'Osrank']
  
  # add csv to inputs object
  inputs.append({
    "path": path,
    "dataframe": df,
    "num_intersections": []
  })

# Init comparison dataframe
N_values = [10, 25, 50, 100, 500]
compare = pd.DataFrame(index=N_values)

# For each input, add ranks to compare dataframe
for N in N_values:
  for container in inputs:
    num_intersections = len(set(inputs[0]["dataframe"].head(N)['Name']).intersection(set(container["dataframe"].head(N)['Name'])))
    container["num_intersections"].append(num_intersections)

# For each input, add ranks to compare dataframe
for container in inputs[1:]:
  compare[container["path"]] = container["num_intersections"]

compare.to_csv(output_path, index=True)
print("Done, wrote to csv", output_path)
