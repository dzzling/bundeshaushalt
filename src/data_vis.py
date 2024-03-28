# %% Imports
import altair as alt
import polars as pl
import re
import os

# %% Read all csv data into one dataframe
df_dict = {}

for filename in os.listdir("../output_data/haushalts_daten"):
    file = pl.read_csv(f"../output_data/haushalts_daten/{filename}", separator=";")
    df_dict[re.findall(r"(.*)(?:\.csv)", filename)[0]] = file

# %%
