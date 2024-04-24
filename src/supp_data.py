# Calculate the supplementary budget and modify original budget plan

# %%
# Imports
import polars as pl
import pathlib

# %%
# Read file
# Use frictionless cli to determine data types of csv files

nhh_file = "nhh_2015_2"
curr_hh_file = "nhh_2015_1"


schema = {
    "einzelplan": pl.String,
    "einzelplan_text": pl.String,
    "einnahmen_ausgaben": pl.String,
    "einnahmen_ausgaben_art": pl.String,
    "kapitel": pl.String,
    "kapitel_text": pl.String,
    "titel": pl.String,
    "funktion": pl.String,
    "titel_text": pl.String,
    "flex": pl.String,
    "seite_neu": pl.String,
    "soll": pl.Int64,
    "seite_bisher": pl.String,
    "bisher": pl.String,
    "titelgruppe": pl.String,
    "tgr_text": pl.String,
}

temp = pl.read_csv(
    f"../input_data/nachtragshaushalte/{nhh_file}.csv", separator=";", schema=schema
)

# %%
# Get old and new values

temp = temp.with_columns(
    pl.col("soll").cast(pl.Int64).alias("soll"),
    pl.col("bisher").cast(pl.Int64).alias("bisher"),
)

# Fix broken function indices
idx = 0
for entry in temp.iter_rows(named=True):
    if len(entry["funktion"]) < 3:
        temp[idx, "funktion"] = "0" + entry["funktion"]
    idx += 1


unconverted_data = temp["funktion"].to_list()
converted_hauptfunktionen = pl.Series([str(number)[0] for number in unconverted_data])

nhh = temp.with_columns(converted_hauptfunktionen.alias("hauptfunktion"))

ctx = pl.SQLContext(register_globals=True, eager_execution=True)

if nhh["einnahmen_ausgaben"][0] is not None:
    nhh_by_hauptfunktion = ctx.execute(
        "SELECT SUM(soll), SUM(bisher), hauptfunktion from nhh WHERE einnahmen_ausgaben='A' OR einnahmen_ausgaben='a' GROUP BY hauptfunktion ORDER BY soll DESC"
    )
else:
    nhh_by_hauptfunktion = ctx.execute(
        "SELECT SUM(soll), SUM(bisher), hauptfunktion from nhh GROUP BY hauptfunktion ORDER BY soll DESC"
    )

print(nhh_by_hauptfunktion)

df_length = nhh_by_hauptfunktion.select(pl.len())["len"].to_list()[0]
has_excess = pl.Series([0] * df_length)
excess_vals = pl.Series([0] * df_length)

# %% Calculate if excess

nhh_by_hauptfunktion = nhh_by_hauptfunktion.with_columns(
    has_excess.alias("has_excess"),
    excess_vals.alias("excess_vals"),
)

idx = 0
for s in nhh_by_hauptfunktion.iter_rows(named=True):
    old_val = s["bisher"]
    new_val = s["soll"]
    if old_val < new_val:
        print(new_val - old_val)
        nhh_by_hauptfunktion[idx, "has_excess"] = True
        nhh_by_hauptfunktion[idx, "excess_vals"] = new_val - old_val
    elif new_val > old_val:
        nhh_by_hauptfunktion[idx, "has_excess"] = False
        nhh_by_hauptfunktion[idx, "excess_vals"] = new_val - old_val
    idx += 1

# %%
# Overwrite original budget plans

schema = {
    "soll": pl.Int64,
    "funktion": pl.String,
    "beschreibung": pl.String,
    "has_excess": pl.Boolean,
    "excess_vals": pl.Int64,
}

if nhh_file[-1:] == "2":
    path_to_curr_file = (
        f"../output_data/haushalts_daten/mit_nachtrag/{curr_hh_file}.csv"
    )
else:
    path_to_curr_file = (
        f"../output_data/haushalts_daten/nach_hauptfunktion/{curr_hh_file}.csv"
    )

curr_data = pl.read_csv(path_to_curr_file, schema=schema, separator=";")

excess_dict = {}
for entry in nhh_by_hauptfunktion.iter_rows(named=True):
    if entry["has_excess"] != 0:
        excess_dict[entry["hauptfunktion"]] = entry["excess_vals"]

idx = 0
for entry in curr_data.iter_rows(named=True):
    if entry["funktion"] in excess_dict:
        if excess_dict[entry["funktion"]] > 0 or curr_data[idx, "has_excess"] is True:
            curr_data[idx, "has_excess"] = True
        else:
            curr_data[idx, "has_excess"] = False
        curr_data[idx, "excess_vals"] = (
            curr_data[idx, "excess_vals"] + excess_dict[entry["funktion"]]
        )
    idx += 1

path: pathlib.Path = f"../output_data/haushalts_daten/mit_nachtrag/{nhh_file}.csv"
curr_data.write_csv(path, separator=";")
# %%
