# Script to create a new version of the dependencies file for each row in the "winners" file
# Each winner's dependency file will have all dependencies except that winner's dependencies
# This way we can see the impact of a certain winner removing its dependencies from the list

import sys
import os
import os.path
import pandas as pd
import numpy as np

# Get filename after making sure it exists
if (len(sys.argv) < 5):
  exit("Please pass the arguments we require (check the Python code)")

# Get params
ranks_csv = sys.argv[1]
n = int(sys.argv[2])
dependencies_meta_csv = sys.argv[3]
dependencies_csv = sys.argv[4]

# Ensure output directory exists
# TODO get from args
output_dir = "cheater_dependencies"
if not os.path.isdir(output_dir):
  os.makedirs(output_dir)

# Load Winners from filename
winners = pd.read_csv(ranks_csv).head(n)
if (len(winners.columns) == 2):
  winners.columns = ['NAME', 'OSRANK']
  dependencies_meta = pd.read_csv(dependencies_meta_csv, index_col="NAME")
  # Add Metadata to Winners
  winners = winners.join(dependencies_meta)
elif (len(winners.columns) == 3):
  winners.columns = ['NAME', 'ID', 'OSRANK']

winners = winners.set_index("NAME")

# Load Dependencies, so we can remove dependencies for each winner
winners_deps = pd.read_csv(dependencies_csv)

# Make one dependency file for each cheater
for index, row in winners.iterrows():
  dependencies_except_this_winners = winners_deps[winners_deps["FROM_ID"]!=row["ID"]]

  # Save to file
  cheater_filename = output_dir + "/cheater." + index + ".deps"
  dependencies_except_this_winners.to_csv(cheater_filename, index=False)
  print(cheater_filename)