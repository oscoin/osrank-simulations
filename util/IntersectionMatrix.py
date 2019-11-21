# Script to compare how projects do in different versions of osrank

import sys
import pandas as pd

# Expects the following arguments
# [0] filename of this script
# [1] filename of the output CSV
# [2] number of projects to keep from each input CSV
# [3]..[N] Paths to input CSVs
# Should be at least 2 CSV paths

# Make sure we have enough params
if (len(sys.argv) < 5):
  exit("Please pass the arguments we require (check the Python code)")

# Save output path
output_path = sys.argv[1]

# Save number of projects to keep
N = int(sys.argv[2])

# Load other params into datafames (no error checking)
inputs = []
for path in sys.argv[3:]:
  df = pd.read_csv(path)
  if (N>0):
    df = df.head(N)
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
labels = sys.argv[3:]
intersection_matrix = pd.DataFrame(index=labels,columns=labels)

# For each pair of inputs, calculate # intersections
for container1 in inputs:
  for container2 in inputs:
    num_intersections = len(set(container1["dataframe"].head(N)['Name']).intersection(set(container2["dataframe"].head(N)['Name'])))
    intersection_matrix[container1["path"]][container2["path"]] = num_intersections

intersection_matrix.to_csv(output_path, index=True)
print("Wrote matrix to csv", output_path)
print(intersection_matrix)
