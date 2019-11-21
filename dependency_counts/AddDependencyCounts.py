# Script to create a new version of the dependencies file for each row in the "winners" file
# Each winner's dependency file will have all dependencies except that winner's dependencies
# This way we can see the impact of a certain winner removing its dependencies from the list

import sys
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Get filename after making sure it exists
if (len(sys.argv) < 2) or not os.path.isfile(sys.argv[1]):
  exit("Please pass the name of an existing winners csv as the first argument")

winners_filename = sys.argv[1] # path to existing csv winners file, with columns "Name", "Id, "Osrank"

# Get filename after making sure it exists
if (len(sys.argv) < 3) or not os.path.isfile(sys.argv[2]):
  exit("Please pass the name of an existing dependencies csv as the second argument")

deps_filename = sys.argv[2] # path to existing csv of dependencies

# Output file
if (len(sys.argv) < 4):
  exit("Please pass the name of the desired output file")

output_filename = sys.argv[3] # path to existing csv of dependencies

# Load Winners from filen
winners = pd.read_csv(winners_filename, index_col="Id")

# Load Dependencies from file
deps = pd.read_csv(deps_filename)

# Count in/out deps for each winner
in_counts = deps.groupby("TO_ID").size().reset_index(name='in_count').set_index("TO_ID")
out_counts = deps.groupby("FROM_ID").size().reset_index(name='out_count').set_index("FROM_ID")
winners = winners.join(in_counts)
winners = winners.join(out_counts)

# Save
winners = winners.reset_index()
winners.to_csv(output_filename, index=False)