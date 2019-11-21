# Script to create a new version of the dependencies file,
#   using only the dependencies for the winners in the given ranks file.

import sys
import pandas as pd

# Expects the following arguments
# [0] filename of this script
# [1] Path to CSV containing the 'winning' projects names as its first column
# [2] Number of winners' dependency information to take into count (all others will be discarded)
# [3] Path to dependencies_meta csv, linking project names to ids
# [4] Path to depdendencies csv, containg FROM_ID, TO_ID columns 
# [5] Path to output file, containing only winners' dependency information

# Make sure we have enough params
if (len(sys.argv) < 6):
  exit("Please pass the arguments we require (check the Python code)")

# Get params (no error or file existence checking!)
winners_csv = sys.argv[1]
n = int(sys.argv[2])
dependencies_meta_csv = sys.argv[3]
dependencies_csv = sys.argv[4]
output_csv = sys.argv[5]

# Load Winners, add metadata if necessary
winners = pd.read_csv(winners_csv).head(n)
if (len(winners.columns) == 2):
  winners.columns = ['NAME', 'OSRANK']
  dependencies_meta = pd.read_csv(dependencies_meta_csv, index_col="NAME")
  # Add Metadata to Winners
  winners = winners.join(dependencies_meta)
elif (len(winners.columns) == 3):
  winners.columns = ['NAME', 'ID', 'OSRANK']

# Load dependencies
dependencies = pd.read_csv(dependencies_csv)

# Remove losers' dependency information
winners_dependencies = dependencies[dependencies["FROM_ID"].isin(winners["ID"])]
winners_dependencies.to_csv(output_csv, index=False)
print(winners_dependencies)