# %%
# Imports
import os
import polars as pl
import re
import pathlib

# %%
# Run through data
df_dict = {}

for filename in os.listdir("../output_data/haushalts_daten/nach_hauptfunktion"):
    file = pl.read_csv(
        f"../output_data/haushalts_daten//nach_hauptfunktion/{filename}", separator=";"
    )
    df_dict[re.findall(r"(.*)(?:\.csv)", filename)[0]] = file

total_df = pl.DataFrame(
    {
        "id": [],
        "year": [],
        "amount": [],
        "function": [],
        "title": [],
        "supp": [],
        "supp_vals": [],
    },
    schema={
        "id": pl.Int64,
        "year": pl.String,
        "amount": pl.Int64,
        "function": pl.Int64,
        "title": pl.String,
        "supp": pl.Boolean,
        "supp_vals": pl.Int64,
    },
)

# %%
# Calculate totals

id = 1
for key, vals in df_dict.items():
    year = re.findall(r"\D*(\d*)\D*", key)[0]
    if year in ["2015", "2016", "2020", "2021", "2023"]:
        continue
    df_length = vals.select(pl.len())["len"].to_list()[0]
    new_data = {
        "id": [],
        "year": [year] * df_length,
        "amount": [],
        "function": [],
        "title": [],
        "supp": [False] * df_length,
        "supp_vals": [0] * df_length,
    }
    for entries in vals.iter_rows(named=True):
        new_data["id"].append(id)
        new_data["amount"].append(entries["soll"])
        new_data["function"].append(entries["hauptfunktion"])
        new_data["title"].append(entries["hauptfunktionstitel"])
        id += 1

    total_df = pl.concat([total_df, pl.DataFrame(new_data)])

# %%
# Add excess vals
supp_dict = {}

for filename in os.listdir("../output_data/haushalts_daten/mit_nachtrag"):
    file = pl.read_csv(
        f"../output_data/haushalts_daten//mit_nachtrag/{filename}", separator=";"
    )
    supp_dict[re.findall(r"(.*)(?:\.csv)", filename)[0]] = file

for key, vals in supp_dict.items():
    year = re.findall(r".*\_(\d*)\_.*", key)[0]
    df_length = vals.select(pl.len())["len"].to_list()[0]
    new_data = {
        "id": [],
        "year": [year] * df_length,
        "amount": [],
        "function": [],
        "title": [],
        "supp": [],
        "supp_vals": [],
    }
    for entries in vals.iter_rows(named=True):
        new_data["id"].append(id)
        new_data["amount"].append(entries["soll"])
        new_data["function"].append(entries["funktion"])
        new_data["title"].append(entries["beschreibung"])
        new_data["supp"].append(entries["has_excess"])
        new_data["supp_vals"].append(entries["excess_vals"])
        id += 1

    total_df = pl.concat([total_df, pl.DataFrame(new_data)])

# %%
# Save total data

path: pathlib.Path = "../output_data/haushalts_daten/hh_total.csv"
total_df.write_csv(path, separator=";")
