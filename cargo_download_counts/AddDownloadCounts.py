# Script to grab top rust projects according to cargo downloads
# Responses should be json and have two top level properties:
# "crates", containing array of crates
# "meta", containing paging information we are currently not using

import sys
import pandas as pd

# Get path of output file
if (len(sys.argv) < 4):
  exit("Please pass the path of the osrank results, the path of the top downloads counts, and the output file name")

ranks_path = sys.argv[1]
downloads_path = sys.argv[2]
output_path = sys.argv[3]

# load and join
ranks = pd.read_csv(ranks_path, index_col="Name")
downloads = pd.read_csv(downloads_path, index_col="name")
ranks_with_downloads = ranks.join(downloads)

print(ranks_with_downloads)

# calculate set operations
intersection = set(ranks.index).intersection(set(downloads.index))
print("ranks/downloads intersection count", len(intersection))

downloads_withtout_ranks = set(downloads.index).difference(set(ranks.index))
print("downloads without ranks", downloads_withtout_ranks)

# write to file
ranks_with_downloads.to_csv(output_path, index=True)
print("Wrote ranks with downloads to", output_path)