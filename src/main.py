# %%
import csv
import json
import os
import polars as pl

# %%
# Funktionstabelle in JSON bereitstellen

with open("../input_data/funktionen_formatted.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]


with open("../output_data/funktionen_formatted.json", "w") as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False)

# %%
# Funltionsdataframe erstellen

with open("../output_data/funktionen_formatted.json", "r") as jsonfile:
    json_data = json.load(jsonfile)
    hauptfunktionen = [x for x in json_data if x["Typ"] == "Hauptfunktion"]

print(hauptfunktionen)

# %%
# Bundeshaushaltsdaten

schema = {
    "einzelplan": pl.Int64,
    "einzelplan_text": pl.String,
    "einnahmen_ausgaben": pl.String,
    "einnahmen_ausgaben_text": pl.String,
    "kapitel": pl.String,
    "kapitel_text": pl.String,
    "titel": pl.String,
    "funktion": pl.Int64,
    "titel_text": pl.String,
    "flex": pl.String,
    "seite": pl.Int64,
    "soll": pl.Int64,
    "titelgruppe": pl.Int64,
    "tgr_text": pl.String,
}

temp = pl.read_csv(
    "../input_data/haushalt_daten/hh_2023.csv",
    separator=";",
    schema=schema,
)

unconverted_data = temp["funktion"].to_list()
converted_data = pl.Series([int(str(number)[0]) for number in unconverted_data])

hh23 = temp.with_columns(converted_data.alias("funktion"))

# %%


# %%
# Addiere Einträge nach Hauptfunktion
ctx = pl.SQLContext(register_globals=True, eager_execution=True)
hh23_small = ctx.execute(
    "SELECT SUM(soll), funktion, titel_text, einnahmen_ausgaben from hh23 WHERE einnahmen_ausgaben='a' GROUP BY funktion ORDER BY soll DESC LIMIT 10"
)
print(hh23_small)

# %%
