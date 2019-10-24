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

filename = sys.argv[1]

# Get N
if (len(sys.argv) < 3):
  exit("Please pass an int for the top N winners as the second argument")

n = int(sys.argv[2])

# Load Winners from filename
winners = pd.read_csv(filename, header=None, names=["NAME", "RANK"])
winners = winners.set_index("NAME")

# Load other files
metadata = pd.read_csv("../osrank-rs-ecosystems/ecosystems/cargo_dependencies_meta.csv", index_col="NAME")
deps = pd.read_csv("../osrank-rs-ecosystems/ecosystems/cargo_dependencies.csv")

# Add Metadata
winners = winners.join(metadata).reset_index().set_index("ID")

# Count in/out deps for each winner
in_counts = deps.groupby("TO_ID").size().reset_index(name='in_count').set_index("TO_ID")
out_counts = deps.groupby("FROM_ID").size().reset_index(name='out_count').set_index("FROM_ID")
winners = winners.join(in_counts)
winners = winners.join(out_counts)

# Now only work with top N winners
top_winners_deps = deps[deps["FROM_ID"].isin(winners.head(n).index) & deps["TO_ID"].isin(winners.head(n).index)]

in_counts = top_winners_deps.groupby("TO_ID").size().reset_index(name='top_in_count').set_index("TO_ID")
out_counts = top_winners_deps.groupby("FROM_ID").size().reset_index(name='top_out_count').set_index("FROM_ID")
winners = winners.join(in_counts)
winners = winners.join(out_counts)

# Save
winners = winners.reset_index()
winners.to_csv("enriched_" + filename)
winners.head(n).to_csv("enriched_top_" + str(n) + "_" + filename)
