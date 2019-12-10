# Script to grab top rust projects according to cargo downloads
# Responses should be json and have two top level properties:
# "crates", containing array of crates
# "meta", containing paging information we are currently not using

import sys
import json
import math
import requests
import pandas as pd

CRATES_TOP_DOWNLOADS_URL = "https://crates.io/api/v1/crates?page=1&per_page=100&sort=downloads"
CRATES_RECENT_DOWNLOADS_URL = "https://crates.io/api/v1/crates?page=1&per_page=100&sort=recent_downloads"
INTERESTING_COLUMNS = ["name", "downloads", "recent_downloads"]

if (len(sys.argv) < 3):
  exit("Please pass the number of downloads requsested and the desired CSV output path")

# important params
number_downloads_requested = int(sys.argv[1])
pages_requested = math.ceil(number_downloads_requested / 100)

output_path = sys.argv[2]

# helper function
def get_crates_array_from_url(url, page_number):
  url_with_page_number = url + "&page=" + str(page_number)
  r = requests.get(url_with_page_number)
  if (r.status_code == 200):
    response_object = json.loads(r.text)
    return response_object["crates"]
  else:
    print("Could not download", url_with_page_number)
    print("Status Code", r.status_code)
    return []

# get all crates from api into one list
top_crates = []
for i in range(1, pages_requested+1):
  print("getting top crates, page", i)
  top_crates.extend(get_crates_array_from_url(CRATES_TOP_DOWNLOADS_URL, i))

# create dataframe from list and write to file
df = pd.DataFrame(top_crates, columns=INTERESTING_COLUMNS)
df.to_csv(output_path, index=False)
print("Wrote top cargo downloads to", output_path)
