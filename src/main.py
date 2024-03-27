# %%
# Imports

import csv
import json
import os
import polars as pl

# %%
# Funktionsdataframe erstellen

with open("../output_data/funktionen_formatted.json", "r") as jsonfile:
    json_data = json.load(jsonfile)
    hauptfunktionen = [x for x in json_data if x["Typ"] == "Hauptfunktion"]


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
    "seite": pl.Int64,
    "soll": pl.Int64,
    "titelgruppe": pl.Int64,
    "tgr_text": pl.String,
}

temp = pl.read_csv(
    "../input_data/haushalt_daten/hh_2022.csv",
    separator=";",
    schema=schema,
)

unconverted_data = temp["funktion"].to_list()
converted_data = pl.Series([str(number)[0] for number in unconverted_data])

hh = temp.with_columns(converted_data.alias("funktion"))

# %%
# Addiere Einträge nach Hauptfunktion
ctx = pl.SQLContext(register_globals=True, eager_execution=True)
hh_aggregated = ctx.execute(
    "SELECT SUM(soll), funktion from hh WHERE einnahmen_ausgaben='A' OR einnahmen_ausgaben='a' GROUP BY funktion ORDER BY soll DESC"
)
total_expenses = ctx.execute(
    "SELECT SUM(soll) from hh WHERE einnahmen_ausgaben='A' OR einnahmen_ausgaben='a'"
)

# %%
# Füge Beschreibung zu aggregierten Daten

with open("../output_data/funktionen_formatted.json", "r") as jsonfile:
    json_data = json.load(jsonfile)
    funktionen_dict = {x["Nummer"]: x["Beschreibung"] for x in json_data}

aggregated_functions = hh_aggregated["funktion"].to_list()
beschreibungen = pl.Series([funktionen_dict[x] for x in aggregated_functions])

hh_complete = hh_aggregated.with_columns(beschreibungen.alias("Hauptfunktion"))

print(hh_complete)
# %%
