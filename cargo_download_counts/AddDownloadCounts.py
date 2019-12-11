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

# calculate set operations
intersection_sizes = [10, 25, 50, 100, 1000]
print("1. intersection count for ranks/downloads")
print("top N projects, # intersections")
for size in intersection_sizes:
  intersection = set(ranks.head(size).index).intersection(set(downloads.head(size).index))
  print(size, len(intersection), sep=",")

# show top downloads that didnt get ranked (werent part of libraries.io data)
downloads_without_ranks = list(set(downloads.index).difference(set(ranks.index)))
print("2. # top cargo downloads without osranks:", len(downloads_without_ranks), "out of", len(downloads))
#print(*downloads_without_ranks,  sep='\n')

# write to file
ranks_with_downloads.to_csv(output_path, index=True)
print("3. Wrote ranks with downloads to", output_path)