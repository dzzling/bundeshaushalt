# %%
# Imports

import json
import polars as pl
import pathlib

# %%
# Define file name

file = "hh_2017"

# %%
# Funktionsdataframe erstellen

with open("../output_data/funktionen_formatted.json", "r") as jsonfile:
    json_data = json.load(jsonfile)
    hauptfunktionen = [x for x in json_data if x["Typ"] == "Hauptfunktion"]
    oberfunktionen = [x for x in json_data if x["Typ"] == "Oberfunktion"]


# %%
# Bundeshaushaltsdaten

schema = {
    "einzelplan": pl.String,
    "einzelplan_text": pl.String,
    "einnahmen_ausgaben": pl.String,
    "einnahmen_ausgaben_text": pl.String,
    "kapitel": pl.String,
    "kapitel_text": pl.String,
    "titel": pl.String,
    "funktion": pl.String,
    "titel_text": pl.String,
    "flex": pl.String,
    "seite": pl.String,
    "soll": pl.Int64,
    "titelgruppe": pl.String,
    "tgr_text": pl.String,
}

temp = pl.read_csv(
    f"../input_data/haushalt_daten/{file}.csv",
    separator=",",
    schema=schema,
)

unconverted_data = temp["funktion"].to_list()
converted_hauptfunktionen = pl.Series([str(number)[0] for number in unconverted_data])
converted_oberfunktionen = pl.Series([str(number[0:2]) for number in unconverted_data])

hh = temp.with_columns(converted_hauptfunktionen.alias("hauptfunktion"))
hh = hh.with_columns(converted_oberfunktionen.alias("oberfunktion"))
print(hh)


# %%
# Addiere Einträge nach Hauptfunktion
ctx = pl.SQLContext(register_globals=True, eager_execution=True)
hh_by_hauptfunktion = ctx.execute(
    "SELECT SUM(soll), hauptfunktion from hh WHERE einnahmen_ausgaben='A' OR einnahmen_ausgaben='a' GROUP BY hauptfunktion ORDER BY soll DESC"
)
hh_by_oberfunktion = ctx.execute(
    "SELECT SUM(soll), oberfunktion from hh WHERE einnahmen_ausgaben='A' OR einnahmen_ausgaben='a' GROUP BY oberfunktion ORDER BY soll DESC"
)

total_expenses = ctx.execute(
    "SELECT SUM(soll) from hh WHERE einnahmen_ausgaben='A' OR einnahmen_ausgaben='a'"
)
print(hh_by_hauptfunktion)

# %%
# Füge Beschreibung zu aggregierten Daten

with open("../output_data/funktionen_formatted.json", "r") as jsonfile:
    json_data = json.load(jsonfile)
    funktionen_dict = {x["Nummer"]: x["Beschreibung"] for x in json_data}

aggregated_mainfunctions = hh_by_hauptfunktion["hauptfunktion"].to_list()
aggregated_lowlevelfunctions = hh_by_oberfunktion["oberfunktion"].to_list()
hauptfunktion_beschreibungen = pl.Series(
    [funktionen_dict[x] for x in aggregated_mainfunctions]
)
oberfunktion_beschreibungen = pl.Series(
    [funktionen_dict[x] for x in aggregated_lowlevelfunctions]
)

hh_complete_by_hauptfunktion = hh_by_hauptfunktion.with_columns(
    hauptfunktion_beschreibungen.alias("hauptfunktionstitel")
)
hh_complete_by_oberfunktion = hh_by_oberfunktion.with_columns(
    oberfunktion_beschreibungen.alias("oberfunktionstitel")
)

print(hh_complete_by_hauptfunktion)
print(hh_complete_by_oberfunktion)

# %%
# Export dataframes as csv

""" path: pathlib.Path = f"../output_data/haushalts_daten/{file}.csv"
hh_complete.write_csv(path, separator=";") """

# %%
