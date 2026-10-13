import json
import csv

# Opens the JSON file ("customerrequests.csv") containing customer request data.
# Writes the data into a new CSV file ("clean_customerrequests.csv") with an added "id" column and a constant "Pending" status.
# The script ensures data is transformed into a well-structured format suitable for further processing or analysis.

import
with open("customerrequests.csv", "r") as f:
    data = json.load(f)

with open("clean_customerrequests.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "phone", "status"])
    for idx, item in enumerate(data, start=1):
        writer.writerow([idx, item["name"], item["phone"], "Pending"])

print("Clean CSV saved as clean_customerrequests.csv")
