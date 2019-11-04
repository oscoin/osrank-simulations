# Script to compare how cheating affects a project's rank and score

import sys
import pandas as pd

# Expects the following arguments
# [0] filename of this script
# [1] filename of the output CSV
# [2] path to primary input CSV
# [3]..[N] Paths to other input CSVs containing "cheating" version for a ranking project
# Should be at least 2 CSV paths

# Make sure we have enough params
if (len(sys.argv) < 4):
  exit("Please pass the arguments we require (check the Python code)")

# Save output path
output_path = sys.argv[1]

# Init result dataframe
compare = pd.DataFrame(columns = ["Name", "Original Osrank Score", "Cheater Osrank Score", "Original Rank", "Cheater Rank"])

# Load original ranks
ranks = pd.read_csv(sys.argv[2], header=None, names=["Name", "Osrank"])

# Construct comparison from cheaters' ranks and scores
for cheater_csv in sys.argv[3:]:
  # Load cheater CSV
  cheater = pd.read_csv(cheater_csv, header=None, names=["Name", "Osrank"])

  # Parse name of this project
  cheater_name = cheater_csv.split('.')[1]

  # Get relevant data from original and cheater dataframes
  original_osrank_score = ranks[ranks["Name"]==cheater_name].iloc[0]["Osrank"]
  cheater_osrank_score = cheater[cheater["Name"]==cheater_name].iloc[0]["Osrank"]

  original_rank = ranks.index[ranks['Name']==cheater_name][0] + 1
  cheater_rank = cheater.index[cheater['Name']==cheater_name][0] + 1
  
  row = {
    "Name" : cheater_name,
    "Original Osrank Score" : original_osrank_score,
    "Cheater Osrank Score" : cheater_osrank_score,
    "Original Rank" : original_rank,
    "Cheater Rank" : cheater_rank
  }

  # Add to result set
  compare = compare.append(row, ignore_index=True)

compare.to_csv(output_path, index=False)
print(compare)