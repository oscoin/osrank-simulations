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
  original_osrank_score = ranks[ranks["Name"]==cheater_name]["Osrank"][0]
  original_rank = ranks.index[ranks['Name']==cheater_name][0] + 1
  cheater_osrank_score = cheater[cheater["Name"]==cheater_name]["Osrank"][0]
  cheater_rank = cheater.index[cheater['Name']==cheater_name][0] + 1
  
  row = [cheater_name, original_osrank_score, cheater_osrank_score, original_rank, cheater_rank]
  print(row)
  # Add to result set
  # TODO add ranks
  compare.loc[-1] = row

compare.to_csv(output_path, index=False)
print(compare)