# %%
import csv
import json
import os

# %%
with open("input_data/funktionen_long_transposed.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

with open("output_data/funktionen_long_transposed.json", "w") as jsonfile:
    json.dump(data, jsonfile)
