# Calculate the supplementary budget and modify original budget plan


# %%
# Imports
import polars as pl

# %%
# Read file
# Use frictionless cli to determine data types of csv files

file = "nhh_2015_1"


schema = {
    "einzelplan": pl.String,
    "einzelplan_text": pl.String,
    "einnahmen_ausgaben": pl.String,
    "einnahmen_ausgaben_art": pl.String,
    "kapitel": pl.String,
    "kapitel_text": pl.String,
    "titel": pl.String,
    "funktion": pl.Int64,
    "titel_text": pl.String,
    "flex": pl.String,
    "seite_neu": pl.String,
    "soll": pl.String,
    "seite_bisher": pl.String,
    "bisher": pl.String,
    "titelgruppe": pl.String,
    "tgr_text": pl.String,
}

temp = pl.read_csv(
    f"../input_data/nachtragshaushalte/{file}.csv", separator=";", schema=schema
)

# %%
# Get old and new values


temp = temp.with_columns(
    pl.col("soll").cast(pl.Int64).alias("soll"),
    pl.col("bisher").cast(pl.Int64).alias("bisher"),
)

unconverted_data = temp["funktion"].to_list()
converted_hauptfunktionen = pl.Series([str(number)[0] for number in unconverted_data])

nhh = temp.with_columns(converted_hauptfunktionen.alias("hauptfunktion"))

ctx = pl.SQLContext(register_globals=True, eager_execution=True)

if nhh["einnahmen_ausgaben"][0] is not None:
    hh_by_hauptfunktion = ctx.execute(
        "SELECT SUM(soll), SUM(bisher), hauptfunktion from nhh WHERE einnahmen_ausgaben='A' OR einnahmen_ausgaben='a' GROUP BY hauptfunktion ORDER BY soll DESC"
    )
else:
    hh_by_hauptfunktion = ctx.execute(
        "SELECT SUM(soll), SUM(bisher), hauptfunktion from nhh GROUP BY hauptfunktion ORDER BY soll DESC"
    )

df_length = hh_by_hauptfunktion.select(pl.len())["len"].to_list()[0]
has_excess = pl.Series([False] * df_length)
excess_vals = pl.Series([0] * df_length)

# %% Calculate if excess

hh_by_hauptfunktion = hh_by_hauptfunktion.with_columns(
    has_excess.alias("has_excess"),
    excess_vals.alias("excess_vals"),
)

idx = 0
for s in hh_by_hauptfunktion.iter_rows(named=True):
    old_val = s["bisher"]
    new_val = s["soll"]
    if old_val < new_val:
        hh_by_hauptfunktion[idx, "has_excess"] = True
        hh_by_hauptfunktion[idx, "excess_vals"] = new_val - old_val
    idx += 1


# if bisher < soll, then label entry in column "extra" as true

# %%
