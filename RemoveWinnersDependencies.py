# Script to create a new version of the dependencies file for each row in the "winners" file
# Each winner's dependency file will have all dependencies except that winner's dependencies
# This way we can see the impact of a certain winner removing its dependencies from the list

import sys
import os
import os.path
import pandas as pd
import numpy as np

# Get filename after making sure it exists
if (len(sys.argv) < 2) or not os.path.isfile(sys.argv[1]):
  exit("Please pass the name of an existing winners csv as the first argument")

filename = sys.argv[1]

# Get N
if (len(sys.argv) < 3):
  exit("Please pass an int for the top N winners as the second argument")

n = int(sys.argv[2])

# Ensure output directory exists
# TODO get from args
output_dir = "cheater_dependencies"
if not os.path.isdir(output_dir):
  os.makedirs(output_dir)

# Load Winners from filename
winners = pd.read_csv(filename, header=None, index_col=0).head(n)

# Add Metadata
metadata = pd.read_csv("../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv", index_col="NAME")
winners = winners.join(metadata)

# Load Dependencies, so we can remove dependencies for each winner
winners_deps = pd.read_csv("../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv")

# Make one dependency file for each cheater
for index, row in winners.iterrows():
  dependencies_except_this_winners = winners_deps[winners_deps["FROM_ID"]!=row["ID"]]

  # Save to file
  cheater_filename = output_dir + "/dependencies_except_" + index + ".csv"
  dependencies_except_this_winners.to_csv(cheater_filename, index=False)
  print(cheater_filename)