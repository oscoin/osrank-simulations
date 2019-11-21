# Script to create a new version of the dependencies file for each row in the original ranks file
# We create a fake dependency list and contribution list for the top 100 ranked projects
# Each of these projects will create 100 fake projects, and depend on them.
# Each of those projects will have 1 contributor
# That contributor will have 1 contribution to the fake project
# And many contributions back to the original project

import sys
import os
import os.path
import pandas as pd
import numpy as np

# Get filename after making sure it exists
if (len(sys.argv) < 4):
  exit("Please pass the arguments we require (check the Python code)")

# Get params
ranks_csv = sys.argv[1]
n = int(sys.argv[2])
dependencies_csv = sys.argv[3]
contributions_csv = sys.argv[4]

# Ensure output directory exists
# TODO get from args
output_dir = "cheater_dependencies"
if not os.path.isdir(output_dir):
  os.makedirs(output_dir)

# Load Winners from filename, assume 3 columns
winners = pd.read_csv(ranks_csv).head(n)
winners.columns = ['NAME', 'ID', 'OSRANK']
winners = winners.set_index("NAME")

# Load Dependencies and Contributions
dependencies = pd.read_csv(dependencies_csv)
contributions = pd.read_csv(contributions_csv)

num_fake_projects = 100
num_fake_contributions_to_real_project = 100
num_fake_contributions_to_fake_project = 1
fake_github_url = "fake_github_url"
fake_github_name = "fake_github_name"

# Make one dependency file and one contribution file for each cheater
for index, row in winners.iterrows():
  # Add fake lines for each fake project
  fake_dependencies_array = []
  fake_contributions_array = []
  for i in range(num_fake_projects):
    fake_project_id = (i+1) * -1
    fake_contributor_name = str(fake_project_id) + "_fake_contributor"

    fake_dependencies_array.append([row["ID"], fake_project_id])
    fake_contributions_array.append([row["ID"], fake_contributor_name, fake_github_url, num_fake_contributions_to_real_project, fake_github_name])
    fake_contributions_array.append([fake_project_id, fake_contributor_name, fake_github_url, num_fake_contributions_to_fake_project, fake_github_name])

  # Turn arrays into dataframes
  fake_dependencies_df = pd.DataFrame(fake_dependencies_array, columns=["FROM_ID", "TO_ID"])
  fake_contributions_df = pd.DataFrame(fake_contributions_array, columns=["ID","MAINTAINER","REPO","CONTRIBUTIONS","NAME"])

  # Concat onto the originals
  cheaters_dependencies = dependencies.append(fake_dependencies_df, ignore_index=True).astype({'FROM_ID': 'int32'})
  cheaters_contributions = contributions.append(fake_contributions_df, ignore_index=True).astype({'ID': 'int32'})

  # Save to file
  cheater_dependencies_filename = output_dir + "/cheater." + index + ".deps"
  cheaters_dependencies.to_csv(cheater_dependencies_filename, index=False)
  print(cheaters_dependencies.tail(10))

  cheater_contributions_filename = output_dir + "/cheater." + index + ".contribs"
  cheaters_contributions.to_csv(cheater_contributions_filename, index=False)
  print(cheaters_contributions.tail(10))

